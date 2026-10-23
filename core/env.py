"""core.env — Load .env configuration and provide runtime environment variables for Python tools."""
import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def load_dotenv():
    env_path = REPO_ROOT / '.env'
    if not env_path.exists():
        return {}
    res = {}
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' not in line:
                continue
            k, v = line.split('=', 1)
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            res[k] = v
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
