"""TransitFare Engine - Regional Bus Fare Calculation and Audit Tool."""

from transit_fare.calculator import FareCalculator
from transit_fare.exceptions import (
    InvalidPassengerError,
    InvalidRouteError,
    TariffRuleError,
    TransitEngineError,
)
from transit_fare.formatter import format_ticket
from transit_fare.models import Passenger, Route, Ticket
from transit_fare.rules import DEFAULT_POLICY, FarePolicy

__version__ = "0.1.0"

__all__ = [
    "FareCalculator",
    "FarePolicy",
    "DEFAULT_POLICY",
    "InvalidPassengerError",
    "InvalidRouteError",
    "Passenger",
    "Route",
    "TariffRuleError",
    "Ticket",
    "TransitEngineError",
    "format_ticket",
    "__version__",
]
