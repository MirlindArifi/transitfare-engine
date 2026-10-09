"""Presentation service for formatting itemized ticket receipts."""

from transit_fare.models import Ticket


def format_ticket(ticket: Ticket) -> str:
    """Format a Ticket object into a readable, itemized terminal receipt.

    Args:
        ticket: A calculated Ticket instance.

    Returns:
        A multiline formatted string representing the ticket.
    """
    separator = "=" * 42
    divider = "-" * 42

    peak_text = "Yes (+€0.50)" if ticket.is_peak else "No"
    discount_sign = f"-€{ticket.discount_amount:.2f}"
    surcharge_sign = f"+€{ticket.peak_surcharge:.2f}"

    lines = [
        separator,
        "          TRANSIT FARE TICKET",
        "     Balkan Regional Bus Transit",
        separator,
        f"Route:        {ticket.route}",
        f"Distance:     {ticket.route.hops} zone hop(s)",
        f"Passenger:    {ticket.passenger}",
        f"Peak Travel:  {peak_text}",
        divider,
        f"Base Fare:                    €{ticket.base_fare:>6.2f}",
        f"Concession Discount:          {discount_sign:>7}",
        f"Peak Surcharge:               {surcharge_sign:>7}",
        divider,
        f"FINAL FARE:                   €{ticket.final_fare:>6.2f}",
        separator,
    ]

    return "\n".join(lines)
