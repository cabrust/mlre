"""Classes and constants that are needed my several radar components."""
import enum


class Severity(enum.IntEnum):
    """Describes the severity of an event."""

    INFO = enum.auto()
    WARNING = enum.auto()
    ERROR = enum.auto()
