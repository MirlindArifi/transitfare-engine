"""Validation service for converting raw CLI inputs into validated domain objects."""

from typing import Tuple

from transit_fare.models import Passenger, Route


def validate_and_create_domain_objects(
    origin_zone: int,
    destination_zone: int,
    passenger_category: str,
) -> Tuple[Route, Passenger]:
    """Validate raw user inputs and instantiate domain objects.

    Args:
        origin_zone: Integer origin zone identifier.
        destination_zone: Integer destination zone identifier.
        passenger_category: String representing passenger category.

    Returns:
        Tuple containing a valid Route and Passenger object.

    Raises:
        ValueError: If any business or domain invariant is violated.
        TypeError: If types cannot be converted.
    """
    route = Route(origin_zone=origin_zone, destination_zone=destination_zone)
    passenger = Passenger(category=passenger_category)
    return route, passenger
