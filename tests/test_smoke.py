"""Smoke test to verify environment and package resolution."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import transit_fare  # noqa: E402


def test_package_version():
    """Verify package imports and has a defined version string."""
    assert transit_fare.__version__ == "0.1.0"
