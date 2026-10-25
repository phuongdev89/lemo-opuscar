"""core.env — Load .env configuration and provide runtime environment variables for Python tools."""
import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def load_dotenv():
    # Shared settings first; optional film-type file overrides only OUTPUT_DIR.
    res = {}
    paths = [REPO_ROOT / '.env']
    selected = os.environ.get('LEMO_ENV_FILE')
    if selected:
        overlay = Path(selected)
        if not overlay.is_absolute():
            overlay = REPO_ROOT / overlay
        if not overlay.is_file():
            raise FileNotFoundError(f'Configuration file not found: {overlay}')
        if overlay.resolve() != paths[0].resolve():
            paths.append(overlay)
    for index, path in enumerate(paths):
        if not path.is_file():
            continue
        for raw in path.read_text(encoding='utf-8-sig').splitlines():
            line = raw.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            key, value = line.split('=', 1)
            key = key.strip()
            if index == 0 or key == 'OUTPUT_DIR':
                res[key] = value.strip().strip('"').strip("'")
    return res


_file_env = load_dotenv()


def get_env(key: str, default: str = '') -> str:
    """Return environment variable value, prioritizing os.environ over .env file."""
    return os.environ.get(key, _file_env.get(key, default))


OUTPUT_DIR = get_env('OUTPUT_DIR', 'films')


def get_project_dir(name: str) -> Path:
    """Get the full Path for a film project given its name or relative path."""
    p = Path(name)
    if p.is_absolute():
        return p
    return REPO_ROOT / OUTPUT_DIR / name
