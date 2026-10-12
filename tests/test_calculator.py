"""Unit tests for the FareCalculator calculation engine."""

import pytest
from transit_fare.calculator import FareCalculator
from transit_fare.models import Passenger, Route


@pytest.fixture
def calculator():
    return FareCalculator()


@pytest.mark.parametrize(
    "origin, dest, category, is_peak, exp_base, exp_discount, exp_surch, exp_final",
    [
        # Regular journeys (0% discount)
        (1, 2, "regular", False, 2.00, 0.00, 0.00, 2.00),
        (1, 2, "regular", True, 2.00, 0.00, 0.50, 2.50),
        (1, 3, "regular", False, 3.50, 0.00, 0.00, 3.50),
        (1, 3, "regular", True, 3.50, 0.00, 0.50, 4.00),
        (1, 4, "regular", False, 5.00, 0.00, 0.00, 5.00),
        (1, 4, "regular", True, 5.00, 0.00, 0.50, 5.50),
        # Student journeys (25% discount off base)
        (1, 2, "student", False, 2.00, 0.50, 0.00, 1.50),
        (1, 2, "student", True, 2.00, 0.50, 0.50, 2.00),
        (1, 3, "student", False, 3.50, 0.88, 0.00, 2.62),
        (1, 3, "student", True, 3.50, 0.88, 0.50, 3.12),
        (1, 4, "student", False, 5.00, 1.25, 0.00, 3.75),
        (1, 4, "student", True, 5.00, 1.25, 0.50, 4.25),
        # Pensioner journeys (35% discount off base)
        (1, 2, "pensioner", False, 2.00, 0.70, 0.00, 1.30),
        (1, 2, "pensioner", True, 2.00, 0.70, 0.50, 1.80),
        (1, 3, "pensioner", False, 3.50, 1.22, 0.00, 2.28),
        (1, 3, "pensioner", True, 3.50, 1.22, 0.50, 2.78),
        (1, 4, "pensioner", False, 5.00, 1.75, 0.00, 3.25),
        (1, 4, "pensioner", True, 5.00, 1.75, 0.50, 3.75),
    ],
)
def test_fare_calculation_matrix(
    calculator,
    origin,
    dest,
    category,
    is_peak,
    exp_base,
    exp_discount,
    exp_surch,
    exp_final,
):
    route = Route(origin, dest)
    passenger = Passenger(category)
    ticket = calculator.calculate(route, passenger, is_peak=is_peak)

    assert ticket.base_fare == exp_base
    assert ticket.discount_amount == exp_discount
    assert ticket.peak_surcharge == exp_surch
    assert ticket.final_fare == exp_final


def test_calculator_invalid_argument_types(calculator):
    route = Route(1, 2)
    passenger = Passenger("regular")

    with pytest.raises(TypeError, match="route must be an instance of Route"):
        calculator.calculate("invalid_route", passenger)  # type: ignore

    with pytest.raises(TypeError, match="passenger must be an instance of Passenger"):
        calculator.calculate(route, "invalid_passenger")  # type: ignore

    with pytest.raises(TypeError, match="is_peak must be a boolean"):
        calculator.calculate(route, passenger, is_peak="yes")  # type: ignore
