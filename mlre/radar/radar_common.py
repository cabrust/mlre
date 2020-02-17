"""Classes and constants that are needed my several radar components."""
import enum
import typing


class Severity(enum.IntEnum):
    """Describes the severity of an event."""

    INFO: int = enum.auto()  # pragma: no mutate
    WARNING: int = enum.auto()  # pragma: no mutate
    ERROR: int = enum.auto()  # pragma: no mutate


class EventIdentifier(typing.NamedTuple):
    """Uniquely identifies an event.

    Members:
        severity: The severity of the event.
        location: Where the event happened.
        description: What happened."""
    severity: Severity
    location: str
    description: str


FreezeFrameMeasurement = typing.Union[str, int, float]
FreezeFrameData = typing.Dict[str, FreezeFrameMeasurement]

__all__ = ["Severity", "EventIdentifier"]
