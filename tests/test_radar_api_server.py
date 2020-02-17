"""Test for radar API server component."""
import typing
import unittest

import mlre
from mlre.radar import radar_api_server, radar_database

_TEST_CONFIGURATION: typing.Dict[str, str] = {
    "TEST_CFG_1": "test_cfg_1_val", "TEST_CFG_2": "test_cfg_2_val"}


class TestRadarAPIServer(unittest.TestCase):
    """Test for radar API server component."""

    def setUp(self) -> None:
        """Creates an instance of the API server to work on."""
        self.database = radar_database.RadarDatabase()
        self.api_server = radar_api_server.create_api_server(
            self.database, _TEST_CONFIGURATION)

        self.api_test_client = self.api_server.test_client().__enter__()  # type: ignore

    def tearDown(self) -> None:
        """Tears down the flask test client."""
        self.api_test_client.__exit__(None, None, None)

    def test_configuration(self) -> None:
        """Check if the supplied configuration was used."""
        for key, value in _TEST_CONFIGURATION.items():
            actual_value: str = typing.cast(
                str, self.api_server.config.get(key))
            self.assertEqual(value, actual_value)

    def test_get_api_version(self) -> None:
        """Test if the reported API and MLRE versions are correct."""
        result = self.api_test_client.get('/version').get_json()
        self.assertEqual('1', result['api'], "There is only this API version.")
        self.assertEqual(mlre.__version__,
                         result['mlre'], "MLRE version should match module.")
