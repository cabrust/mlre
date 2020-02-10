"""Test for the radar API connection component."""
import json
import unittest
import urllib.parse
import uuid

import responses
from mlre.radar import radar_common, radar_connection

_TEST_HOSTNAME = "test_hostname"
_TEST_ENDPOINT = "https://api.test_url.org/"
_TEST_SESSION_UUID = uuid.uuid1()
_TEST_EVENT_SEVERITY = radar_common.Severity.INFO
_TEST_EVENT_DESCRIPTION = "This is a test event"
_TEST_EVENT_LOCATION = __name__
_TEST_EVENT_FREEZE_FRAME = {"test_data": 1.23456789}
_TEST_ENVIRONMENT = {"ENV1": "env1_test", "ENV2": "ENV2"}


def _report_test_client_info(connection: radar_connection.Connection) -> None:
    connection.report_client_info(_TEST_HOSTNAME,
                                  _TEST_ENVIRONMENT)


def _report_test_event(connection: radar_connection.Connection) -> None:
    connection.report_event(
        _TEST_EVENT_SEVERITY,
        _TEST_EVENT_LOCATION,
        _TEST_EVENT_DESCRIPTION,
        _TEST_EVENT_FREEZE_FRAME)


class PatchedPostRequestRadarConnectionTestCase(unittest.TestCase):
    """Base class for test cases which patches request.post to always return ok."""

    def setUp(self) -> None:
        self.connection: radar_connection.Connection = radar_connection.Connection(
            _TEST_ENDPOINT, _TEST_SESSION_UUID)

        # Add mocks for API calls
        responses.add(responses.POST,
                      urllib.parse.urljoin(_TEST_ENDPOINT, "report_event"),
                      status=200)
        responses.add(responses.POST,
                      urllib.parse.urljoin(
                          _TEST_ENDPOINT, "report_client_info"),
                      status=200)


class TestRadarConnectionSessionFlow(PatchedPostRequestRadarConnectionTestCase):
    """Test case for radar API connection component's session flow.

    The connection component should enforce reporting the client info exactly once
    before allowing events to be reported."""

    @responses.activate
    def test_can_only_report_client_info_once(self) -> None:
        """Should fail if the client is able to report its info more than once."""
        _report_test_client_info(self.connection)
        with self.assertRaises(ValueError):
            _report_test_client_info(self.connection)

    @responses.activate
    def test_needs_to_report_client_info(self) -> None:
        """Should fail if client can report an event without reporting client info beforehand."""
        with self.assertRaises(ValueError):
            _report_test_event(self.connection)

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
            _TEST_ENDPOINT, "report_client_info"), responses.calls[0].request.url)

        # Decode request again
        decoded_request = json.loads(responses.calls[0].request.body)

        self.assertEqual(_TEST_HOSTNAME, decoded_request["hostname"])
        self.assertEqual(_TEST_SESSION_UUID, uuid.UUID(
            decoded_request["session"]))
        self.assertEqual(_TEST_ENVIRONMENT,
                         decoded_request["environment_variables"])

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
            _TEST_ENDPOINT, "report_event"), responses.calls[1].request.url)

        raise NotImplementedError("This test is mostly missing!")
