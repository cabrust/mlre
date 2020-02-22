import unittest
from unittest import mock

from mlre.radar import radar_app, radar_database, radar_frontend


class TestRadarAPIServerDefaultApp(unittest.TestCase):
    """Test for radar API server default app method."""

    def setUp(self) -> None:
        """Hooks up the API server factory to mocking."""
        self.create_api_server_patcher = mock.patch(
            'mlre.radar.radar_api_server.create_api_server')
        self.patched_create_api_server = self.create_api_server_patcher.start()

        self.create_frontend_blueprint_patcher = mock.patch(
            'mlre.radar.radar_frontend.create_frontend_blueprint')
        self.patched_create_frontend_blueprint = self.create_frontend_blueprint_patcher.start()

    def tearDown(self) -> None:
        """Tears down the factory mock."""
        self.create_api_server_patcher.stop()
        self.create_frontend_blueprint_patcher.stop()

    def test_default_app(self) -> None:
        """Tests if the default app creator uses the correct call."""
        radar_app.create_default_app()  # type: ignore

        # Method should have been called only once
        self.assertEqual(1, self.patched_create_api_server.call_count)
        self.assertEqual(1, self.patched_create_frontend_blueprint.call_count)

        # Extract method arguments
        create_api_arguments, _ = self.patched_create_api_server.call_args
        create_frontend_arguments, _ = self.patched_create_frontend_blueprint.call_args

        # Test if the supplied argument is an actual database.
        self.assertTrue(isinstance(
            create_api_arguments[0], radar_database.RadarDatabase))
