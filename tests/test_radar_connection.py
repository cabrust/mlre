"""Test for the radar API connection component."""
import json
import unittest
import urllib.parse
import uuid

import responses

import mlre
import test_radar_common
from mlre.radar import radar_common, radar_connection


def _report_test_client_info(connection: radar_connection.Connection) -> None:
    """Reports sample client info to connection."""
    connection.report_client_info(test_radar_common.TEST_CLIENT_INFO)


def _report_test_event(connection: radar_connection.Connection) -> None:
    """Reports sample client event to connection."""
    connection.report_event(
        test_radar_common.TEST_EVENT_IDENTIFIER,
        test_radar_common.TEST_EVENT_FREEZE_FRAME)


class PatchedPostRequestRadarConnectionTestCase(unittest.TestCase):
    """Base class for test cases which patches request.post to always return ok."""

    def setUp(self) -> None:
        self.connection: radar_connection.Connection = radar_connection.Connection(
            test_radar_common.TEST_ENDPOINT, test_radar_common.TEST_SESSION_UUID)

        # Add mocks for API calls
        responses.add(responses.POST,
                      urllib.parse.urljoin(
                          test_radar_common.TEST_ENDPOINT, "report_event"),
                      status=200)
        responses.add(responses.POST,
                      urllib.parse.urljoin(
                          test_radar_common.TEST_ENDPOINT, "report_client_info"),
                      status=200)


class TestRadarConnectionSessionFlow(PatchedPostRequestRadarConnectionTestCase):
    """Test case for radar API connection component's session flow.

    The connection component should enforce reporting the client info exactly once
    before allowing events to be reported."""

    @responses.activate
    def test_can_only_report_client_info_once(self) -> None:
        """Should fail if the client is able to report its info more than once."""
        _report_test_client_info(self.connection)
        with self.assertRaises(ValueError) as error:
            _report_test_client_info(self.connection)
        self.assertEqual(
            "This method should only be called once per session.", error.exception.args[0])

    @responses.activate
    def test_needs_to_report_client_info(self) -> None:
        """Should fail if client can report an event without reporting client info beforehand."""
        with self.assertRaises(ValueError) as error:
            _report_test_event(self.connection)
        self.assertEqual(
            "Make sure to report the client information before reporting any events.",
            error.exception.args[0])

    @responses.activate
    def test_can_report_event_after_reporting_client_info(self) -> None:
        """Should fail if client cannot report an event after reporting client info beforehand."""
        _report_test_client_info(self.connection)


class TestRadarConnectionRequestBodies(PatchedPostRequestRadarConnectionTestCase):
    """Test case for radar API connection component's request body contents."""

    @responses.activate
    def test_report_client_info(self) -> None:
        """Check the request body of a client info report for compliance."""
        _report_test_client_info(self.connection)

        self.assertEqual(1, len(responses.calls),
                         "Client should have made one call.")

        # Test URL
        self.assertEqual(urllib.parse.urljoin(
            test_radar_common.TEST_ENDPOINT, "report_client_info"), responses.calls[0].request.url)

        # Decode request again
        decoded_request = json.loads(responses.calls[0].request.body)

        self.assertEqual(test_radar_common.TEST_CLIENT_INFO,
                         radar_common.ClientInfo(*decoded_request["client_info"]))
        self.assertEqual(test_radar_common.TEST_SESSION_UUID, uuid.UUID(
            decoded_request["session"]))

    @responses.activate
    def test_report_event(self) -> None:
        """Check the request body of an event report for compliance."""

        # Need to report client info first
        _report_test_client_info(self.connection)

        _report_test_event(self.connection)

        self.assertEqual(2, len(responses.calls),
                         "Client should have made two calls.")

        # Test URL
        self.assertEqual(urllib.parse.urljoin(
            test_radar_common.TEST_ENDPOINT, "report_event"), responses.calls[1].request.url)

        # Decode request again
        decoded_request = json.loads(responses.calls[1].request.body)

        self.assertEqual(test_radar_common.TEST_SESSION_UUID, uuid.UUID(
            decoded_request["session"]))
        self.assertEqual(test_radar_common.TEST_EVENT_IDENTIFIER, radar_common.EventIdentifier(
            *decoded_request["event_identifier"]))
        self.assertEqual(test_radar_common.TEST_EVENT_FREEZE_FRAME,
                         decoded_request["freeze_frame"])


class TestRadarConnectionVersionDecode(unittest.TestCase):
    """Test case for the version API call."""

    def setUp(self) -> None:
        self.connection: radar_connection.Connection = radar_connection.Connection(
            test_radar_common.TEST_ENDPOINT, test_radar_common.TEST_SESSION_UUID)

        # Add mocks for API calls
        responses.add(responses.GET,
                      urllib.parse.urljoin(
                          test_radar_common.TEST_ENDPOINT, "version"),
                      json={'api': '1', 'mlre': mlre.__version__},
                      status=200)

    @responses.activate
    def test_version_call_api_correct(self) -> None:
        """Test if the API call to retrieve version information is correct."""
        actual_api_version = self.connection.get_api_version()

        # Test URL
        self.assertEqual(urllib.parse.urljoin(
            test_radar_common.TEST_ENDPOINT, "version"), responses.calls[0].request.url)

        # Test result
        self.assertEqual('1', actual_api_version,
                         "Parsed API version should be correct.")

    @responses.activate
    def test_version_call_mlre_correct(self) -> None:
        """Test if the API call to retrieve version information is correct."""
        actual_mlre_version = self.connection.get_mlre_version()

        # Test URL
        self.assertEqual(urllib.parse.urljoin(
            test_radar_common.TEST_ENDPOINT, "version"), responses.calls[0].request.url)

        # Test result
        self.assertEqual(mlre.__version__, actual_mlre_version,
                         "Parsed MLRE version should be correct.")
