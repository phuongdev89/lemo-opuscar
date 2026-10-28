"""QA entry point for all film genres; math loads .env.math last."""
from math_qa import main

if __name__ == '__main__':
    raise SystemExit(main(default_film_type='general'))
