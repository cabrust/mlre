"""Database access layer for radar event and client info."""
import typing

from . import radar_common

_EventDataDict = typing.Dict[radar_common.EventIdentifier,
                             typing.List[radar_common.FreezeFrameData]]  # pragma: no mutate


class RadarDatabase:
    """Represents a database for radar event and client info."""

    def __init__(self) -> None:
        self._event_data: _EventDataDict = dict()

    @property
    def event_identifiers(self) -> typing.Sequence[radar_common.EventIdentifier]:
        """Gets all events uniquely identified by the severity/location/description triplet."""
        return list(self._event_data.keys())

    def insert_event(
            self,
            event_identifier: radar_common.EventIdentifier,
            freeze_frame: radar_common.FreezeFrameData,
    ) -> None:
        """Inserts an event into the database.

        If the event already exists, the freeze frames are merged.

        Args:
            event_identifier: Unique identifier of the event.
            freeze_frame: A dictionary of helpful measurements.
        """
        if event_identifier not in self.event_identifiers:
            self._event_data[event_identifier] = [freeze_frame]
        else:
            self._event_data[event_identifier] += [freeze_frame]

    def event(self, event_identifier: radar_common.EventIdentifier)\
            -> typing.List[radar_common.FreezeFrameData]:
        """Returns the freeze frame data matching the given identifier.

        Args:
            event_identifier: Unique identifier of the event.

        Returns:
            The freeze frame data matching the event identifier.
        """
        return self._event_data[event_identifier]


__all__ = ["RadarDatabase"]
