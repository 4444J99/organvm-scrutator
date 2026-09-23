"""Deterministic guard for the hosted daily scan workflow."""

import json
import sys
from pathlib import Path


_INVALID_COUNT = "visibility index total_plans must be a non-negative integer"


def read_total_plans(index_path: Path) -> int:
    """Return the indexed plan count, treating a missing index as an empty scan."""
    if not index_path.is_file():
        return 0

    payload = json.loads(index_path.read_text())
    if not isinstance(payload, dict):
        raise TypeError(_INVALID_COUNT)

    total = payload.get("total_plans", 0)
    if isinstance(total, bool) or not isinstance(total, int) or total < 0:
        raise ValueError(_INVALID_COUNT)
    return total


def should_publish_scan(index_path: Path) -> bool:
    """Only non-empty hosted scans may run mutating follow-up steps."""
    return read_total_plans(index_path) > 0


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: python -m organvm_scrutator.ci_guard <visibility-index.json>")

    index_path = Path(sys.argv[1])
    total = read_total_plans(index_path)
    print(f"total_plans={total}")
    print(f"publish_scan={'true' if total > 0 else 'false'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
