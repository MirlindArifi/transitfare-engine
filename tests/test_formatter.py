"""Unit tests for ticket receipt formatting."""

from transit_fare.formatter import format_ticket
from transit_fare.models import Passenger, Route, Ticket


def test_format_ticket_contains_all_key_line_items():
    route = Route(1, 4)
    passenger = Passenger("student")
    ticket = Ticket(
        route=route,
        passenger=passenger,
        base_fare=5.00,
        discount_amount=1.25,
        peak_surcharge=0.50,
        final_fare=4.25,
        is_peak=True,
    )

    rendered = format_ticket(ticket)

    assert "TRANSIT FARE TICKET" in rendered
    assert "Prishtina" in rendered
    assert "Prizren" in rendered
    assert "3 zone hop(s)" in rendered
    assert "Student" in rendered
    assert "Yes (+€0.50)" in rendered
    assert "€  5.00" in rendered
    assert "-€1.25" in rendered
    assert "+€0.50" in rendered
    assert "€  4.25" in rendered


def test_format_ticket_off_peak():
    route = Route(1, 2)
    passenger = Passenger("regular")
    ticket = Ticket(
        route=route,
        passenger=passenger,
        base_fare=2.00,
        discount_amount=0.00,
        peak_surcharge=0.00,
        final_fare=2.00,
        is_peak=False,
    )

    rendered = format_ticket(ticket)
    assert "Peak Travel:  No" in rendered
    assert "+€0.00" in rendered
    assert "-€0.00" in rendered
