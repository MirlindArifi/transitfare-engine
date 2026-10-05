"""Fare calculation engine for the TransitFare Engine."""

from transit_fare.models import Passenger, Route, Ticket
from transit_fare.rules import DEFAULT_POLICY, FarePolicy


class FareCalculator:
    """Calculates transit fares based on route, passenger, and time of day."""

    def __init__(self, policy: FarePolicy = DEFAULT_POLICY) -> None:
        """Initialize the calculator with a tariff policy."""
        if not isinstance(policy, FarePolicy):
            raise TypeError("policy must be an instance of FarePolicy.")
        self.policy: FarePolicy = policy

    def calculate(
        self, route: Route, passenger: Passenger, is_peak: bool = False
    ) -> Ticket:
        """Calculate the itemized ticket fare for a journey.

        Args:
            route: A valid Route object.
            passenger: A valid Passenger object.
            is_peak: Boolean indicating whether peak-hour surcharge applies.

        Returns:
            A populated, immutable Ticket instance.

        Raises:
            TypeError: If input arguments are of incorrect types.
        """
        if not isinstance(route, Route):
            raise TypeError(
                f"route must be an instance of Route. " f"Got {type(route).__name__}."
            )
        if not isinstance(passenger, Passenger):
            raise TypeError(
                f"passenger must be an instance of Passenger. "
                f"Got {type(passenger).__name__}."
            )
        if not isinstance(is_peak, bool):
            raise TypeError("is_peak must be a boolean.")

        # 1. Retrieve base fare by route hops
        base_fare = self.policy.get_base_fare(route.hops)

        # 2. Calculate concession discount
        discount_rate = self.policy.get_discount_rate(passenger.category)
        discount_amount = round(base_fare * discount_rate, 2)

        # 3. Calculate subtotal after concession
        subtotal = round(base_fare - discount_amount, 2)

        # 4. Determine peak-hour surcharge
        peak_surcharge = self.policy.peak_surcharge if is_peak else 0.0

        # 5. Calculate final payable fare
        final_fare = round(subtotal + peak_surcharge, 2)

        return Ticket(
            route=route,
            passenger=passenger,
            base_fare=base_fare,
            discount_amount=discount_amount,
            peak_surcharge=peak_surcharge,
            final_fare=final_fare,
            is_peak=is_peak,
        )
