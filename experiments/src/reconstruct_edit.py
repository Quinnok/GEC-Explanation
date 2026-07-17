from __future__ import annotations

import argparse
import json

from reconstruction_models import get_reconstructor, reconstruction_to_json


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--explanation", required=True)
    parser.add_argument("--error-type", default="UNK")
    parser.add_argument("--model", default="explicit_edit_pattern")
    args = parser.parse_args()
    reconstructor = get_reconstructor(args.model)
    edit = reconstructor.reconstruct(args.source, args.explanation, error_type=args.error_type)
    print(json.dumps(reconstruction_to_json(edit), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

