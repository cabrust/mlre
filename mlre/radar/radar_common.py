"""Classes and constants that are needed my several radar components."""
import enum
import typing


class Severity(enum.IntEnum):
    """Describes the severity of an event."""

    INFO = enum.auto()
    WARNING = enum.auto()
    ERROR = enum.auto()


class EventIdentifier(typing.NamedTuple):
    """Uniquely identifies an event.

    Members:
        severity: The severity of the event.
        location: Where the event happened.
        description: What happened."""
    severity: Severity
    location: str
    description: str


FreezeFrameData = typing.Dict[str, typing.Any]  # pragma: no mutate

__all__ = ["Severity", "EventIdentifier"]
