"""Tests for the radar session object."""
import os
import socket
import unittest
from unittest import mock

import test_radar_common
from mlre.radar import radar_common, radar_session


class TestRadarSession(unittest.TestCase):
    """Tests for the radar session object."""

    def setUp(self) -> None:
        """Sets up the APIClient mock."""
        self.patcher = mock.patch('mlre.radar.radar_api_client.APIClient')
        self.patched_api_client_type = self.patcher.start()

    def tearDown(self) -> None:
        """Tears down the APIClient mock."""
        self.patcher.stop()

    def test_server_default(self) -> None:
        """Tests if the Session uses localhost by default."""
        if 'RADAR_SERVER' in os.environ.keys():
            del os.environ['RADAR_SERVER']

        with radar_session.RadarSession():
            self.assertEqual(1, self.patched_api_client_type.call_count)

            # Test correct hostname
            self.assertEqual('https://127.0.0.1:5000/',
                             self.patched_api_client_type.call_args[0][0])

    def test_server_environ(self) -> None:
        """Tests if the Session uses the environment variable RADAR_SERVER."""
        os.environ['RADAR_SERVER'] = test_radar_common.TEST_ENDPOINT

        with radar_session.RadarSession():
            self.assertEqual(1, self.patched_api_client_type.call_count)

            # Test correct hostname
            self.assertEqual(test_radar_common.TEST_ENDPOINT,
                             self.patched_api_client_type.call_args[0][0])

    def test_reports_client_info(self) -> None:
        """Tests if the Session reports client information after connecting."""
        self.test_server_default()

        self.assertEqual(
            1, self.patched_api_client_type.return_value.report_client_info.call_count)

        # Check for correctness of client info
        actual_client_info: radar_common.ClientInfo =\
            self.patched_api_client_type.return_value.report_client_info.call_args[
                0][0]
        expected_client_info = radar_common.ClientInfo(
            socket.gethostname(), os.environ)  # type: ignore

        self.assertEqual(expected_client_info, actual_client_info)

    def test_reports_session_start_event(self) -> None:
        """Tests if the Session reports a start event after connecting."""
        if 'RADAR_SERVER' in os.environ.keys():
            del os.environ['RADAR_SERVER']

        with radar_session.RadarSession():
            self.assertEqual(
                1, self.patched_api_client_type.return_value.report_event.call_count)

            # Check for correctness of start event
            actual_identifier: radar_common.EventIdentifier =\
                self.patched_api_client_type.return_value.report_event.call_args[
                    0][0]
            expected_identifier = radar_common.EventIdentifier(
                severity=radar_common.Severity.INFO,
                location="mlre.radar.radar_session",
                description="Session started")

        self.assertEqual(expected_identifier, actual_identifier)

    def test_reports_session_end_event(self) -> None:
        """Tests if the Session reports an end event when exiting the session."""

        # Session should be concluded after this
        self.test_server_default()

        # 2 because it includes both start and end events
        self.assertEqual(
            2, self.patched_api_client_type.return_value.report_event.call_count)

        # Check for correctness of end event
        actual_identifier: radar_common.EventIdentifier =\
            self.patched_api_client_type.return_value.report_event.call_args[
                0][0]
        expected_identifier = radar_common.EventIdentifier(
            severity=radar_common.Severity.INFO,
            location="mlre.radar.radar_session",
            description="Session ended")

        self.assertEqual(expected_identifier, actual_identifier)
