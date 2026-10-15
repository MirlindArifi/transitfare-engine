# TransitFare Engine — Balkan Regional Transit Fare & Concession Engine

[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Linter: Flake8](https://img.shields.io/badge/linter-flake8-yellow.svg)](https://flake8.pycqa.org/)
[![Tests: Pytest](https://img.shields.io/badge/tests-pytest-green.svg)](https://docs.pytest.org/)

A deterministic command-line transit fare calculation and ticket audit tool designed for regional bus operators in the Western Balkans (modeled after intercity lines such as the Prishtina–Prizren corridor).

---

## 1. Real-World Problem

In regional transit across the Western Balkans, bus conductors and station clerks frequently calculate multi-zone fares, student/pensioner concessions, and peak-hour surcharges by hand or using fragmented paper tariff tables. This manual process causes:
* **Calculation discrepancies**: Human errors during busy boarding windows.
* **Inconsistent concession application**: Variable discounts applied to eligible passengers.
* **Audit mismatches**: Discrepancies between cash collected by conductors and ticket manifests audited at central stations.

**TransitFare Engine** provides a consistent, auditable, and deterministic calculation engine that validates journey constraints, calculates exact concession rates, applies peak-hour surcharges, and generates itemized ticket receipts.

---

## 2. Core Architecture & Data Flow

The application enforces a strict separation of concerns: input validation, domain modeling, tariff calculation, and receipt presentation are isolated from each other.

```text
       [ CLI Arguments (-o, -d, -p, --peak) ]
                         ↓
             [ Input Validator Service ]
                         ↓
      [ Instantiate Domain Objects: Route, Passenger ]
                         ↓
  [ FareCalculator Engine + FarePolicy (Dependency Injected) ]
                         ↓
         [ Immutable Ticket Value Object ]
                         ↓
            [ Receipt Formatter Service ]
                         ↓
           [ Itemized Terminal Output ]
