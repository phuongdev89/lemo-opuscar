"""Shared image routing for all film types; installed skills supply API adapters."""
import argparse
import importlib.util
import io
import json
import os
from pathlib import Path
import re
import tempfile
from contextlib import contextmanager

ROOT = Path(__file__).resolve().parents[1]


def read_config(path):
    values = {}
    for raw in path.read_text(encoding='utf-8-sig').splitlines():
        line = raw.strip()
        if line and not line.startswith('#') and '=' in line:
            key, value = line.split('=', 1)
            values[key.strip()] = value.strip().strip('\"\'')
    return values


def skill(name, script):
    for root in (Path.home()/'.agents/skills', Path.home()/'.codex/skills'):
        path = root/name/'scripts'/script
        if path.is_file():
            spec = importlib.util.spec_from_file_location(name.replace('-', '_'), path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
    raise FileNotFoundError(f'Installed skill missing: {name}')


class MissingConfiguration(ValueError):
    pass


def merged_config(adapter):
    # Skill-global file, process-global values, then project overrides.
    path = Path(adapter.__file__).resolve()
    values = {}
    for source in (path.parents[3]/'.env', path.parents[1]/'.env'):
        if source.is_file():
            values.update(read_config(source))
    values.update({k: v for k, v in os.environ.items()
                   if k.startswith(('API_IMAGE_', 'AI_IMAGE_', 'MUSE_', 'MUSEAI_IMAGE_')) or k == 'AI_TIMEOUT'})
    if (ROOT/'.env').is_file():
        values.update(read_config(ROOT/'.env'))
    return values


@contextmanager
def skill_config(adapter):
    values = merged_config(adapter)
    if hasattr(adapter, 'load_candidate_env'):
        original = adapter.load_candidate_env
        adapter.load_candidate_env = lambda: values.copy()
        try:
            yield
        finally:
            adapter.load_candidate_env = original
    else:
        keys = {k for k in values if k.startswith(('MUSE_', 'MUSEAI_IMAGE_'))}
        previous = {k: os.environ.get(k) for k in keys}
        old = Path.cwd()
        try:
            os.chdir(ROOT)
            os.environ.update({k: values[k] for k in keys})
            yield
        finally:
            os.chdir(old)
            for key, value in previous.items():
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value


def api_configs(adapter):
    with skill_config(adapter):
        configs = adapter.resolve_providers()
    issues = [{'provider': c['provider'], 'issues': adapter.config_issues(c)} for c in configs]
    missing = [item for item in issues if item['issues']]
    if missing:
        raise MissingConfiguration(json.dumps(missing))
    return configs


def generate(provider, cfg, prompt, destination, size):
    if provider == 'muse-image':
        adapter = skill('muse-image', 'muse_image.py')
        with skill_config(adapter):
            try:
                endpoint, key, model, limit, interval = adapter.load_config()
            except ValueError:
                raise MissingConfiguration(json.dumps([{'skill': 'muse-image', 'issues': ['Check MUSE_ENDPOINT_URL, MUSE_API_KEY and optional timeout/poll settings in global or project configuration']}])) from None
        data = adapter.request_json(endpoint+'/images/generations', key, limit,
                                    {'model': model, 'prompt': prompt, 'size': size, 'async': True})
        data = adapter.poll_task(data, endpoint, key, limit, interval)
        adapter.save_result(data, endpoint, key, limit, destination)
        return model
    adapter = skill('api-image', 'generate_image.py')
    old = Path.cwd()
    try:
        os.chdir(ROOT)
        configs = api_configs(adapter)
        response, selected, attempts = adapter.run_providers(
            configs, prompt=prompt, ref_data_uri=None, size=size,
            quality='auto', image_detail='high')
    finally:
        os.chdir(old)
    cfg['api_attempts'] = attempts
    if response is None:
        if selected is None:
            raise RuntimeError('HTTP 503 API providers exhausted')
        raise ValueError('API stopped; inspect attempts before any further submission')
    image, _, _, reported_model = response
    destination.write_bytes(image)
    cfg['api_provider'] = selected['provider']
    return reported_model or selected['model']


def failure_action(message):
    low = message.lower()
    if any(word in low for word in ('timeout', 'timed out', 'connection', 'kết nối')):
        return 'pending-unknown-submission'
    if any(word in low for word in ('safety', 'policy', 'moderation', 'content_filter')):
        return 'stop-safety'
    match = re.search(r'HTTP\s+(\d{3})', message, re.I)
    if match and int(match[1]) in (401, 402, 403, 429, 500, 502, 503):
        return 'fallback'
    return 'stop-review-error'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prompt-file', type=Path)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--size', default='1792x1024', help='Requested API image size')
    parser.add_argument('--cover', action='store_true', help='Normalize to 1280x720 PNG under 2 MB')
    parser.add_argument('--builtin-unavailable', choices=['not-present', 'unsupported', 'service', 'quota', 'access'],
                        help='Required evidence before entering API fallback; never use for safety or unknown timeout')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    cfg = {}
    if args.dry_run:
        adapter = skill('api-image', 'generate_image.py')
        old = Path.cwd()
        try:
            os.chdir(ROOT)
            configs = api_configs(adapter)
        finally:
            os.chdir(old)
        print(json.dumps({'skills': ['image-generate', 'api-image', 'muse-image'],
                          'builtin': 'agent must inspect host tools',
                          'api_providers': [{'provider': c['provider'], 'issues': adapter.config_issues(c)} for c in configs],
                          'configuration_order': 'global then project overrides', 'network_called': False}, indent=2))
        return 0
    if not args.builtin_unavailable:
        parser.error('Use image-generate built-in first; API requires --builtin-unavailable with a verified reason')
    statuses = [{'provider': p, 'configured': True} for p in ('api-image', 'muse-image')]
    if not args.prompt_file or not args.output:
        parser.error('--prompt-file and --output required')
    prompt = args.prompt_file.read_text(encoding='utf-8-sig').strip()
    if not prompt:
        parser.error('Empty prompt')
    from PIL import Image, ImageOps
    output = args.output.resolve()
    if output.exists():
        parser.error('Output already exists; choose another path')
    output.parent.mkdir(parents=True, exist_ok=True)
    result = {'status': 'pending', 'prompt': prompt, 'attempts': [
        {'provider': 'image-generate', 'reason': args.builtin_unavailable}]}
    for status in statuses:
        provider = status['provider']
        if not status['configured']:
            result['attempts'].append({'provider': provider, 'reason': 'missing-configuration'})
            continue
        with tempfile.TemporaryDirectory() as temporary:
            raw = Path(temporary)/'image.png'
            try:
                model = generate(provider, cfg, prompt, raw, args.size)
                with Image.open(raw) as image:
                    image.load()
                    image = image.convert('RGB')
                    if args.cover:
                        image = ImageOps.fit(image, (1280, 720), method=Image.Resampling.LANCZOS)
                    dimensions = list(image.size)
                    buffer = io.BytesIO()
                    image.save(buffer, format='PNG', optimize=True)
                    if args.cover and len(buffer.getvalue()) >= 2*1024*1024:
                        image.quantize(colors=256).save(buffer := io.BytesIO(), format='PNG', optimize=True)
                    if args.cover and len(buffer.getvalue()) >= 2*1024*1024:
                        raise ValueError('Cover exceeds 2 MB')
                    output.write_bytes(buffer.getvalue())
                result.update(status='generated-needs-visual-review', provider=provider, model=model,
                              output=str(output), size=dimensions)
                result['attempts'].append({'provider': provider, 'status': 'generated'})
                if provider == 'api-image':
                    result.update(api_attempts=cfg.get('api_attempts', []), api_provider=cfg.get('api_provider'))
                break
            except Exception as exc:
                # Persist categories only: upstream exception messages can contain secrets.
                action = 'missing-configuration' if isinstance(exc, MissingConfiguration) else failure_action(str(exc))
                if isinstance(exc, MissingConfiguration):
                    result['configuration_issues'] = json.loads(str(exc))
                if provider == 'api-image':
                    result['api_attempts'] = cfg.get('api_attempts', [])
                result['attempts'].append({'provider': provider, 'reason': action, 'error_type': type(exc).__name__})
                if action != 'fallback':
                    break
    output.with_suffix('.result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['status'].startswith('generated') else 1


if __name__ == '__main__':
    raise SystemExit(main())
