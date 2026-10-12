"""Unit tests for domain models (Route, Passenger, Ticket)."""

import pytest
from transit_fare.models import Passenger, Route, Ticket


class TestRoute:
    """Tests for Route domain entity."""

    def test_valid_route_creation_and_hops(self):
        route = Route(origin_zone=1, destination_zone=4)
        assert route.origin_zone == 1
        assert route.destination_zone == 4
        assert route.hops == 3
        assert "Prishtina" in str(route)
        assert "Prizren" in str(route)

    def test_route_reverse_hops(self):
        route = Route(origin_zone=4, destination_zone=1)
        assert route.hops == 3

    def test_route_rejects_intra_zone_travel(self):
        with pytest.raises(ValueError, match="Intra-zone travel is not supported"):
            Route(origin_zone=2, destination_zone=2)

    @pytest.mark.parametrize(
        "origin, destination",
        [
            (0, 2),  # origin below min
            (5, 2),  # origin above max
            (1, 0),  # destination below min
            (1, 5),  # destination above max
        ],
    )
    def test_route_rejects_out_of_bounds_zones(self, origin, destination):
        with pytest.raises(ValueError, match="zone must be between 1 and 4"):
            Route(origin_zone=origin, destination_zone=destination)

    def test_route_rejects_non_integer_types(self):
        with pytest.raises(TypeError, match="Zone identifiers must be integers"):
            Route(origin_zone="1", destination_zone=2)  # type: ignore


class TestPassenger:
    """Tests for Passenger domain entity."""

    @pytest.mark.parametrize(
        "raw_category, expected_concession",
        [
            ("regular", False),
            ("REGULAR", False),
            ("student", True),
            (" Student ", True),
            ("pensioner", True),
        ],
    )
    def test_passenger_normalization_and_concessions(
        self, raw_category, expected_concession
    ):
        passenger = Passenger(category=raw_category)
        assert passenger.has_concession is expected_concession

    def test_passenger_rejects_invalid_category(self):
        with pytest.raises(ValueError, match="Invalid passenger category 'tourist'"):
            Passenger(category="tourist")

    def test_passenger_rejects_non_string(self):
        with pytest.raises(TypeError, match="Passenger category must be a string"):
            Passenger(category=123)  # type: ignore


class TestTicket:
    """Tests for Ticket value object."""

    def test_ticket_rejects_negative_amounts(self):
        route = Route(1, 2)
        passenger = Passenger("regular")
        with pytest.raises(ValueError, match="cannot be negative"):
            Ticket(
                route=route,
                passenger=passenger,
                base_fare=-1.0,
                discount_amount=0.0,
                peak_surcharge=0.0,
                final_fare=1.0,
                is_peak=False,
            )
