"""Test for radar API server component."""
import typing
import unittest

from mlre.radar import radar_api_server, radar_database

_TEST_CONFIGURATION:  typing.Dict[str, str] = {
    "TEST_CFG_1": "test_cfg_1_val", "TEST_CFG_2": "test_cfg_2_val"}


class TestRadarAPIServer(unittest.TestCase):
    def setUp(self) -> None:
        """Creates an instance of the API server to work on."""
        self.database = radar_database.RadarDatabase()
        self.api_server = radar_api_server.create_api_server(
            self.database, _TEST_CONFIGURATION)

    """Test for radar API server component."""

    def test_configuration(self) -> None:
        """This test checks if the supplied configuration was used."""
        for key, value in _TEST_CONFIGURATION.items():
            actual_value: str = typing.cast(
                str, self.api_server.config.get(key))
            self.assertEqual(value, actual_value)
