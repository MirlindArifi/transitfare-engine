"""Domain models for the TransitFare Engine."""

from dataclasses import dataclass
from typing import ClassVar, Dict, Set


class Route:
    """Represents a regional transit route between two numeric zones."""

    MIN_ZONE: ClassVar[int] = 1
    MAX_ZONE: ClassVar[int] = 4

    # Authentic regional corridor landmark mapping
    ZONE_NAMES: ClassVar[Dict[int, str]] = {
        1: "Prishtina",
        2: "Lipjan/Shtime",
        3: "Suharekë",
        4: "Prizren",
    }

    def __init__(self, origin_zone: int, destination_zone: int) -> None:
        """Initialize and validate a transit route.

        Raises:
            TypeError: If zones are not integers.
            ValueError: If zones are out of bounds or origin equals destination.
        """
        if not isinstance(origin_zone, int) or not isinstance(destination_zone, int):
            raise TypeError("Zone identifiers must be integers.")

        if not (self.MIN_ZONE <= origin_zone <= self.MAX_ZONE):
            raise ValueError(
                f"Origin zone must be between " f"{self.MIN_ZONE} and {self.MAX_ZONE}."
            )

        if not (self.MIN_ZONE <= destination_zone <= self.MAX_ZONE):
            raise ValueError(
                f"Destination zone must be between "
                f"{self.MIN_ZONE} and {self.MAX_ZONE}."
            )

        if origin_zone == destination_zone:
            raise ValueError(
                "Intra-zone travel is not supported. "
                "Origin and destination must differ."
            )

        self.origin_zone: int = origin_zone
        self.destination_zone: int = destination_zone

    @property
    def hops(self) -> int:
        """Calculate the absolute number of zone boundaries crossed."""
        return abs(self.destination_zone - self.origin_zone)

    @property
    def origin_name(self) -> str:
        """Return the friendly name of the origin zone."""
        return self.ZONE_NAMES[self.origin_zone]

    @property
    def destination_name(self) -> str:
        """Return the friendly name of the destination zone."""
        return self.ZONE_NAMES[self.destination_zone]

    def __str__(self) -> str:
        return (
            f"Zone {self.origin_zone} ({self.origin_name}) → "
            f"Zone {self.destination_zone} ({self.destination_name})"
        )

    def __repr__(self) -> str:
        return (
            f"Route(origin_zone={self.origin_zone}, "
            f"destination_zone={self.destination_zone})"
        )


class Passenger:
    """Represents a transit passenger and their concession status."""

    VALID_CATEGORIES: ClassVar[Set[str]] = {
        "regular",
        "student",
        "pensioner",
    }

    def __init__(self, category: str) -> None:
        """Initialize and validate a passenger.

        Raises:
            TypeError: If category is not a string.
            ValueError: If category is not one of the allowed categories.
        """
        if not isinstance(category, str):
            raise TypeError("Passenger category must be a string.")

        normalized_category = category.strip().lower()

        if normalized_category not in self.VALID_CATEGORIES:
            allowed = ", ".join(sorted(self.VALID_CATEGORIES))
            message = (
                f"Invalid passenger category '{category}'. " f"Allowed: {allowed}."
            )
            raise ValueError(message)

        self.category: str = normalized_category

    @property
    def has_concession(self) -> bool:
        """Return True if passenger qualifies for a concession discount."""
        return self.category in {"student", "pensioner"}

    def __str__(self) -> str:
        return self.category.capitalize()

    def __repr__(self) -> str:
        return f"Passenger(category='{self.category}')"


@dataclass(frozen=True)
class Ticket:
    """Immutable data record representing a calculated fare transaction."""

    route: Route
    passenger: Passenger
    base_fare: float
    discount_amount: float
    peak_surcharge: float
    final_fare: float
    is_peak: bool

    def __post_init__(self) -> None:
        """Validate monetary consistency upon instantiation."""
        for field_name, amount in [
            ("base_fare", self.base_fare),
            ("discount_amount", self.discount_amount),
            ("peak_surcharge", self.peak_surcharge),
            ("final_fare", self.final_fare),
        ]:
            if amount < 0:
                message = f"{field_name} cannot be negative. Got {amount}."
                raise ValueError(message)
