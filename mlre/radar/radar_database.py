"""Database access layer for radar event and client info."""
import typing
import uuid

from . import radar_common

_EventDataList = typing.List[typing.Tuple[
    radar_common.EventIdentifier,
    typing.List[typing.Tuple[uuid.UUID, radar_common.FreezeFrameData]]]]

_ClientInfoDict = typing.Dict[uuid.UUID,
                              radar_common.ClientInfo]


class RadarDatabase:
    """Represents a database for radar event and client info."""

    def __init__(self) -> None:
        self._event_data: _EventDataList = list()
        self._client_info: _ClientInfoDict = dict()

    def event_identifiers(self) -> typing.Sequence[typing.Tuple[int, radar_common.EventIdentifier]]:
        """Gets all events uniquely identified by the severity/location/description triplet."""
        return [(i, event_identifier) for i, (event_identifier, _) in enumerate(self._event_data)]

    def insert_event(
            self,
            session_id: uuid.UUID,
            event_identifier: radar_common.EventIdentifier,
            freeze_frame: radar_common.FreezeFrameData,
    ) -> int:
        """Inserts an event into the database.

        If the event already exists, the freeze frames are merged.

        Args:
            session_id: Unique session identifier.
            event_identifier: Unique identifier of the event.
            freeze_frame: A dictionary of helpful measurements.
        """
        all_identifiers = [event_identifier for (
            event_identifier, _) in self._event_data]
        if event_identifier not in all_identifiers:
            new_index = len(self._event_data)
            self._event_data.insert(
                new_index, (event_identifier, [(session_id, freeze_frame)]))
            return new_index

        # Already exists
        index = all_identifiers.index(event_identifier)
        self._event_data[index] = (
            self._event_data[index][0], self._event_data[index][1] + [(session_id, freeze_frame)])
        return index

    def event(self, event_index: int)\
            -> typing.Tuple[radar_common.EventIdentifier,
                            typing.List[typing.Tuple[uuid.UUID, radar_common.FreezeFrameData]]]:
        """Returns the freeze frame data matching the given identifier.

        Args:
            event_index: Database index of the event.

        Returns:
            The freeze frame data matching the event identifier.
        """
        return self._event_data[event_index]

    def insert_client_info(self, session_id: uuid.UUID,
                           client_info: radar_common.ClientInfo) -> None:
        """Inserts client info for a session into the database.

        Args:
            session_id: Unique session identifier.
            client_info: Client information structure."""

        self._client_info[session_id] = client_info

    def client_info(self, session_id: uuid.UUID) -> radar_common.ClientInfo:
        """Gets client info associated with a session id from the database."""
        return self._client_info[session_id]


__all__ = ["RadarDatabase"]
