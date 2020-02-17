"""Handles to client->server connection."""
import urllib.parse
import uuid

import requests

from . import radar_common


class Connection:
    """Represents an active connection to a radar server."""

    def __init__(self,
                 endpoint_url: str,
                 session_uuid: uuid.UUID):
        """Connects to a radar server.

        Args:
            endpoint_url: URL to send requests to.
            session_uuid: UUID (self-generated) of the current session.
        """
        self._endpoint_url: str = endpoint_url
        self._session_uuid: uuid.UUID = session_uuid
        self._has_reported_client_info: bool = False

    def report_client_info(
            self,
            client_info: radar_common.ClientInfo) -> None:
        """Reports information about the client to the server.

        This method should only be called once per session, and before
        any events are reported.

        Args:
            client_info: Client information object.
        """
        if self._has_reported_client_info:
            raise ValueError(
                "This method should only be called once per session.")

        request_url = urllib.parse.urljoin(
            self._endpoint_url, "report_client_info")
        request_body = {"session": str(self._session_uuid),
                        "client_info": client_info}

        requests.post(request_url, json=request_body)

        # Remember having reported client information
        self._has_reported_client_info = True

    def report_event(
            self,
            event_identifier: radar_common.EventIdentifier,
            freeze_frame: radar_common.FreezeFrameData,
    ) -> None:
        """Reports an event to the server.

        Make sure to report the client information before reporting any events.

        Args:
            event_identifier: Unique identifier of the event.
            freeze_frame: A dictionary of helpful measurements.
        """
        if not self._has_reported_client_info:
            raise ValueError(
                "Make sure to report the client information before reporting any events.")

        request_url = urllib.parse.urljoin(self._endpoint_url, "report_event")
        request_body = {"session": str(self._session_uuid),
                        "event_identifier": event_identifier,
                        "freeze_frame": freeze_frame}

        requests.post(request_url, json=request_body)


__all__ = ["Connection"]
