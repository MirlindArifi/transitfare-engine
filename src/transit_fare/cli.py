"""Command-Line Interface parser and controller for TransitFare Engine."""

import argparse
import sys
from typing import List, Optional

from transit_fare.calculator import FareCalculator
from transit_fare.validator import validate_and_create_domain_objects


def build_parser() -> argparse.ArgumentParser:
    """Build and configure the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="transitfare",
        description="Balkan Regional Transit Fare & Concession Engine",
        epilog=(
            "Supported zones: 1 (Prishtina), 2 (Lipjan/Shtime), "
            "3 (Suharekë), 4 (Prizren)"
        ),
    )

    parser.add_argument(
        "-o",
        "--origin",
        type=int,
        required=True,
        help="Origin zone number (1-4)",
    )
    parser.add_argument(
        "-d",
        "--destination",
        type=int,
        required=True,
        help="Destination zone number (1-4)",
    )
    parser.add_argument(
        "-p",
        "--passenger",
        type=str,
        default="regular",
        help="Passenger category: regular (default), student, pensioner",
    )
    parser.add_argument(
        "--peak",
        action="store_true",
        default=False,
        help="Apply peak-hour surcharge (+€0.50)",
    )

    return parser


def run_cli(args: Optional[List[str]] = None) -> int:
    """Parse CLI arguments, execute calculation, and print output.

    Returns:
        Exit code: 0 on success, 1 on domain or validation error.
    """
    parser = build_parser()
    parsed_args = parser.parse_args(args)

    try:
        route, passenger = validate_and_create_domain_objects(
            origin_zone=parsed_args.origin,
            destination_zone=parsed_args.destination,
            passenger_category=parsed_args.passenger,
        )
        calculator = FareCalculator()
        ticket = calculator.calculate(
            route=route, passenger=passenger, is_peak=parsed_args.peak
        )

        print(f"Calculated Fare: €{ticket.final_fare:.2f}")
        return 0

    except (ValueError, TypeError) as err:
        print(f"Error: {err}", file=sys.stderr)
        return 1
