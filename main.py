"""TransitFare Engine CLI entry point."""

import sys
from pathlib import Path

# Ensure src directory is present on Python search path when executing directly
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from transit_fare.cli import run_cli  # noqa: E402


def main() -> None:
    """Run CLI entry point and exit with return code."""
    sys.exit(run_cli())


if __name__ == "__main__":
    main()
