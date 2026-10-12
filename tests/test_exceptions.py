"""Unit tests verifying domain exception hierarchy and behavior."""

import pytest
from transit_fare.exceptions import (
    InvalidPassengerError,
    InvalidRouteError,
    TariffRuleError,
    TransitEngineError,
)
from transit_fare.models import Passenger, Route
from transit_fare.rules import DEFAULT_POLICY


def test_exception_inheritance():
    """Verify that domain exceptions inherit from TransitEngineError and ValueError."""
    assert issubclass(InvalidRouteError, TransitEngineError)
    assert issubclass(InvalidRouteError, ValueError)

    assert issubclass(InvalidPassengerError, TransitEngineError)
    assert issubclass(InvalidPassengerError, ValueError)

    assert issubclass(TariffRuleError, TransitEngineError)
    assert issubclass(TariffRuleError, ValueError)


def test_route_raises_invalid_route_error():
    with pytest.raises(InvalidRouteError):
        Route(1, 1)

    with pytest.raises(InvalidRouteError):
        Route(1, 99)


def test_passenger_raises_invalid_passenger_error():
    with pytest.raises(InvalidPassengerError):
        Passenger("unknown_category")


def test_rules_raises_tariff_rule_error():
    with pytest.raises(TariffRuleError):
        DEFAULT_POLICY.get_base_fare(99)
