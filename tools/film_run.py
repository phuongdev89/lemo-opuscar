"""Run a production command with persistent, complete, secret-redacted output."""
import argparse
from datetime import datetime, timezone
import html
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
import uuid


def redact(text):
    for key, value in os.environ.items():
        if len(value) >= 4 and re.search(r'KEY|TOKEN|SECRET|PASSWORD|AUTHORIZATION', key, re.I):
            text = text.replace(value, '[REDACTED]')
    return re.sub(r'(?i)(bearer\s+|(?:api[_-]?key|token|password|secret)\s*[=:]\s*)[^\s,;]+',
                  r'\1[REDACTED]', text)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--film', required=True, type=Path)
    parser.add_argument('--cwd', type=Path, default=Path.cwd())
    parser.add_argument('--phase', required=True)
    parser.add_argument('command', nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)
    command = args.command[1:] if args.command[:1] == ['--'] else args.command
    if not command:
        parser.error('command required after --')
    logs = args.film.resolve() / 'project' / 'logs' / 'commands'
    logs.mkdir(parents=True, exist_ok=True)
    run = logs / (datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S') + '-' + uuid.uuid4().hex[:12])
    run.mkdir()
    record = dict(started_at=datetime.now(timezone.utc).isoformat(), phase=args.phase,
                  cwd=redact(str(args.cwd.resolve())), command=[redact(x) for x in command],
                  status='running', output='output.txt', stderr='merged into output.txt')
    metadata = run / 'command.json'
    metadata.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
    start = time.monotonic()
    code = 127
    with (run / 'output.txt').open('w', encoding='utf-8') as output:
        try:
            process = subprocess.Popen(command, cwd=args.cwd, stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
            with process.stdout:
                for line in process.stdout:
                    clean = redact(line)
                    output.write(clean)
                    output.flush()
                    print(clean, end='', flush=True)
            code = process.wait()
        except OSError as error:
            output.write(redact(str(error)) + '\n')
    record.update(ended_at=datetime.now(timezone.utc).isoformat(),
                  duration_seconds=round(time.monotonic() - start, 3), exit_code=code,
                  status='completed' if code == 0 else 'failed')
    metadata.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
    # Browser-readable full transcript; never interpret command output as markup.
    (run / 'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Command log</title>'
        + '<pre>' + html.escape(json.dumps(record, ensure_ascii=False, indent=2)) + '</pre>'
        + '<a href="output.txt">Full stdout + stderr</a><pre>'
        + html.escape((run / 'output.txt').read_text(encoding='utf-8')) + '</pre>', encoding='utf-8')
    print(f'Command log: {run}')
    return code


if __name__ == '__main__':
    sys.exit(main())
