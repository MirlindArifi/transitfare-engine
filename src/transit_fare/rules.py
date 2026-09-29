"""Tariff configuration and fare rules for the TransitFare Engine."""

from dataclasses import dataclass, field
from typing import Dict


@dataclass(frozen=True)
class FarePolicy:
    """Encapsulates tariff structure and concession rules for a network."""

    # Base fare by number of zone hops crossed
    hop_fares: Dict[int, float] = field(
        default_factory=lambda: {
            1: 2.00,  # e.g., Zone 1 -> Zone 2 (Lipjan)
            2: 3.50,  # e.g., Zone 2 -> Zone 4 (Prizren)
            3: 5.00,  # e.g., Zone 1 -> Zone 4 (Prishtina -> Prizren)
        }
    )

    # Concession discount percentage off base fare
    concession_rates: Dict[str, float] = field(
        default_factory=lambda: {
            "regular": 0.00,
            "student": 0.25,
            "pensioner": 0.35,
        }
    )

    # Surcharge applied during morning/evening commuter rush
    peak_surcharge: float = 0.50

    def get_base_fare(self, hops: int) -> float:
        """Retrieve the base fare for a given number of zone hops.

        Raises:
            ValueError: If no fare is defined for requested hops.
        """
        if hops not in self.hop_fares:
            valid_hops = ", ".join(str(h) for h in sorted(self.hop_fares))
            msg = (
                f"No tariff defined for {hops} zone hop(s). "
                f"Supported hops: {valid_hops}."
            )
            raise ValueError(msg)
        return self.hop_fares[hops]

    def get_discount_rate(self, category: str) -> float:
        """Retrieve concession discount rate for a passenger category.

        Raises:
            ValueError: If category has no defined discount rate.
        """
        normalized = category.strip().lower()
        if normalized not in self.concession_rates:
            valid_cats = ", ".join(sorted(self.concession_rates))
            msg = (
                f"Unknown concession category '{category}'. "
                f"Supported: {valid_cats}."
            )
            raise ValueError(msg)
        return self.concession_rates[normalized]


# Default regional policy for Balkan transit corridor
DEFAULT_POLICY = FarePolicy()
