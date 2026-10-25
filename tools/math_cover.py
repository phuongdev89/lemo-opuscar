"""Compatibility entry point for math covers; shared .env image configuration."""
import sys
from film_image import main

if __name__ == '__main__':
    if '--cover' not in sys.argv:
        sys.argv.append('--cover')
    raise SystemExit(main())
