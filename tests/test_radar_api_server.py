"""Test for radar API server component."""
import typing
import unittest
from unittest import mock

import mlre
import test_radar_common
from mlre.radar import radar_api_server, radar_database

_TEST_CONFIGURATION: typing.Dict[str, str] = {
    "TEST_CFG_1": "test_cfg_1_val", "TEST_CFG_2": "test_cfg_2_val"}


class TestRadarAPIServer(unittest.TestCase):
    """Test for radar API server component."""

    def setUp(self) -> None:
        """Creates an instance of the API server to work on and a mock database."""

        # Create mocked database
        self.patcher = mock.patch('mlre.radar.radar_database.RadarDatabase')
        patched_database_type = self.patcher.start()
        self.database = patched_database_type()

        # Start test client
        self.api_server = radar_api_server.create_api_server(
            self.database, _TEST_CONFIGURATION)

        self.api_test_client = self.api_server.test_client().__enter__()  # type: ignore

    def tearDown(self) -> None:
        """Tears down the flask test client and database mock."""
        self.api_test_client.__exit__(None, None, None)
        self.patcher.stop()

    def test_configuration(self) -> None:
        """Check if the supplied configuration was used."""
        for key, value in _TEST_CONFIGURATION.items():
            actual_value: str = typing.cast(
                str, self.api_server.config.get(key))
            self.assertEqual(value, actual_value)

    def test_get_api_version(self) -> None:
        """Test if the reported API and MLRE versions are correct."""
        response = self.api_test_client.get('/version')

        self.assertEqual(200, response.status_code)

        result = response.get_json()
        self.assertEqual('1', result['api'], "There is only this API version.")
        self.assertEqual(mlre.__version__,
                         result['mlre'], "MLRE version should match module.")

    def test_report_event(self) -> None:
        """Test if the event reporting API calls the database correctly."""
        request_body = {"session_id": str(test_radar_common.TEST_SESSION_UUID),
                        "event_identifier": test_radar_common.TEST_EVENT_IDENTIFIER,
                        "freeze_frame": test_radar_common.TEST_EVENT_FREEZE_FRAME}

        response = self.api_test_client.post(
            '/report_event', json=request_body)

        self.assertEqual(200, response.status_code)

        self.assertEqual(1, len(self.database.method_calls),
                         "Number of database calls should be 1")

        # Test if method was called correctly
        target_method, arguments, _ = self.database.method_calls[0]

        self.assertEqual('insert_event', target_method)
        self.assertEqual(test_radar_common.TEST_SESSION_UUID, arguments[0])
        self.assertEqual(test_radar_common.TEST_EVENT_IDENTIFIER, arguments[1])
        self.assertEqual(
            test_radar_common.TEST_EVENT_FREEZE_FRAME, arguments[2])

    def test_report_client_info(self) -> None:
        """Test if the client info reporting API calls the database correctly."""
        request_body = {"session_id": str(test_radar_common.TEST_SESSION_UUID),
                        "client_info": test_radar_common.TEST_CLIENT_INFO}

        response = self.api_test_client.post(
            '/report_client_info', json=request_body)

        self.assertEqual(200, response.status_code)

        self.assertEqual(1, len(self.database.method_calls),
                         "Number of database calls should be 1")

        # Test if method was called correctly
        target_method, arguments, _ = self.database.method_calls[0]

        self.assertEqual('insert_client_info', target_method)
        self.assertEqual(test_radar_common.TEST_SESSION_UUID, arguments[0])
        self.assertEqual(test_radar_common.TEST_CLIENT_INFO, arguments[1])


class TestRadarAPIServerDefaultApp(unittest.TestCase):
    """Test for radar API server default app method."""

    def setUp(self) -> None:
        """Hooks up the API server factory to mocking."""
        self.patcher = mock.patch(
            'mlre.radar.radar_api_server.create_api_server')
        self.patched_method = self.patcher.start()

    def tearDown(self) -> None:
        """Tears down the factory mock."""
        self.patcher.stop()

    def test_default_app(self) -> None:
        """Tests if the default app creator uses the correct call."""
        radar_api_server.create_default_app()  # type: ignore

        # Method should have been called only once
        self.assertEqual(1, self.patched_method.call_count)

        # Extract method arguments
        arguments, _ = self.patched_method.call_args

        # Test if the supplied argument is an actual database.
        self.assertTrue(isinstance(arguments[0], radar_database.RadarDatabase))
