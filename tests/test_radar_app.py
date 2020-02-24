"""Test for radar app entry point."""
import unittest
from unittest import mock

from mlre.radar import radar_app, radar_database


class TestRadarApp(unittest.TestCase):
    """Test for radar app entry point."""

    def setUp(self) -> None:
        """Hooks up the API server factory to mocking."""
        self.create_api_server_blueprint_patcher = mock.patch(
            'mlre.radar.radar_api_server.create_api_server_blueprint')
        self.patched_create_api_server_blueprint = self.create_api_server_blueprint_patcher.start()

        self.create_frontend_blueprint_patcher = mock.patch(
            'mlre.radar.radar_frontend.create_frontend_blueprint')
        self.patched_create_frontend_blueprint = self.create_frontend_blueprint_patcher.start()

        self.radar_app = radar_app.create_default_app()  # type: ignore

    def tearDown(self) -> None:
        """Tears down the factory mock."""
        self.create_api_server_blueprint_patcher.stop()
        self.create_frontend_blueprint_patcher.stop()

    def test_create_default_app(self) -> None:
        """Tests if the default app creator uses the correct call."""

        # Method should have been called only once
        self.assertEqual(
            1, self.patched_create_api_server_blueprint.call_count)
        self.assertEqual(1, self.patched_create_frontend_blueprint.call_count)

        # Extract method arguments
        create_api_arguments, _ = self.patched_create_api_server_blueprint.call_args
        create_frontend_arguments, _ = self.patched_create_frontend_blueprint.call_args

        # Test if the supplied argument is an actual database.
        self.assertTrue(isinstance(
            create_api_arguments[0], radar_database.RadarDatabase))
        self.assertTrue(isinstance(
            create_frontend_arguments[0], radar_database.RadarDatabase))
