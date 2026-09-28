"""TransitFare Engine CLI entry point."""

import sys
from pathlib import Path

# Ensure src is on Python path when running main.py directly
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from transit_fare import __version__  # noqa: E402


def main() -> None:
    """Run TransitFare Engine entry point."""
    print("=" * 45)
    print(f"TransitFare Engine v{__version__}")
    print("Balkan Regional Transit Fare & Concession Engine")
    print("=" * 45)
    print("Ready for domain initialization.")


if __name__ == "__main__":
    main()
