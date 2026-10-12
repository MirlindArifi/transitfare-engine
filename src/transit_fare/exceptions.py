"""Domain exception hierarchy for the TransitFare Engine."""


class TransitEngineError(Exception):
    """Base exception for all domain errors raised by TransitFare Engine."""


class InvalidRouteError(TransitEngineError, ValueError):
    """Raised when route parameters or zone boundaries are invalid."""


class InvalidPassengerError(TransitEngineError, ValueError):
    """Raised when a passenger category is unrecognized or invalid."""


class TariffRuleError(TransitEngineError, ValueError):
    """Raised when tariff lookup rules fail or policy rates are missing."""
