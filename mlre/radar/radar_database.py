"""Database access layer for radar event and client info."""
import typing
import uuid

from . import radar_common

_EventDataDict = typing.Dict[radar_common.EventIdentifier,
                             typing.List[radar_common.FreezeFrameData]]

_ClientInfoDict = typing.Dict[uuid.UUID,
                              radar_common.ClientInfo]


class RadarDatabase:
    """Represents a database for radar event and client info."""

    def __init__(self) -> None:
        self._event_data: _EventDataDict = dict()
        self._client_info: _ClientInfoDict = dict()

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

    def insert_client_info(self, session_id: uuid.UUID,
                           client_info: radar_common.ClientInfo) -> None:
        """Inserts client info for a session into the database.

        Args:
            session_id: Unique session identifier.
            client_info: Client information structure."""

        self._client_info[session_id] = client_info

    def client_info(self, session_id: uuid.UUID) -> typing.Optional[radar_common.ClientInfo]:
        """Gets client info associated with a session id from the database."""
        return self._client_info[session_id]


__all__ = ["RadarDatabase"]
