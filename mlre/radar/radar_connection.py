"""Handles to client->server connection."""
import typing
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
        self._endpoint_url = endpoint_url
        self._session_uuid = session_uuid
        self._has_reported_client_info = False

    def report_client_info(
            self,
            hostname: str,
            environment_variables: typing.Dict[str, str]) -> None:
        """Reports information about the client to the server.

        This method should only be called once per session, and before
        any events are reported.

        Args:
            hostname: The client's hostname.
            environment_variables: A dictionary of all the client's environment variables.
        """
        if self._has_reported_client_info:
            raise ValueError(
                "This method should only be called once per session.")

        request_url = urllib.parse.urljoin(
            self._endpoint_url, "report_client_info")
        request_body = {"session": str(self._session_uuid),
                        "hostname": hostname,
                        "environment_variables": environment_variables}

        requests.post(request_url, json=request_body)

        # Remember having reported client information
        self._has_reported_client_info = True

    def report_event(
            self,
            severity: radar_common.Severity,
            location: str,
            description: str,
            freeze_frame: typing.Dict[str, typing.Any],
    ) -> None:
        """Reports an event to the server.

        Make sure to report the client information before reporting any events.

        Args:
            severity: The severity of the event.
            location: Where the event happened.
            description: What happened.
            freeze_frame: A dictionary of helpful measurements.
        """
        if not self._has_reported_client_info:
            raise ValueError(
                "Make sure to report the client information before reporting any events.")

        request_url = urllib.parse.urljoin(self._endpoint_url, "report_event")
        request_body = {"session": str(self._session_uuid),
                        "severity": severity,
                        "location": location,
                        "description": description,
                        "freeze_frame": freeze_frame}

        requests.post(request_url, json=request_body)
