"""Unit tests for fare policy and tariff rules."""

import pytest
from transit_fare.rules import DEFAULT_POLICY, FarePolicy


def test_default_policy_base_fares():
    assert DEFAULT_POLICY.get_base_fare(1) == 2.00
    assert DEFAULT_POLICY.get_base_fare(2) == 3.50
    assert DEFAULT_POLICY.get_base_fare(3) == 5.00


def test_default_policy_discounts():
    assert DEFAULT_POLICY.get_discount_rate("regular") == 0.00
    assert DEFAULT_POLICY.get_discount_rate("student") == 0.25
    assert DEFAULT_POLICY.get_discount_rate("pensioner") == 0.35


def test_invalid_hop_lookup_raises():
    with pytest.raises(ValueError, match="No tariff defined for 4 zone hop"):
        DEFAULT_POLICY.get_base_fare(4)


def test_invalid_category_lookup_raises():
    with pytest.raises(ValueError, match="Unknown concession category"):
        DEFAULT_POLICY.get_discount_rate("military")


def test_custom_fare_policy():
    custom = FarePolicy(
        hop_fares={1: 1.00},
        concession_rates={"regular": 0.0, "student": 0.50},
        peak_surcharge=1.00,
    )
    assert custom.get_base_fare(1) == 1.00
    assert custom.get_discount_rate("student") == 0.50
    assert custom.peak_surcharge == 1.00
