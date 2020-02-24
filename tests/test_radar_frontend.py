"""Tests for the radar frontend component."""
from flask import Flask

import snapshottest
import test_radar_common
from mlre.radar import radar_frontend


class RadarFrontendTestCase(test_radar_common.MockedDatabaseTestCase, snapshottest.TestCase):
    """Tests for the radar frontend component."""

    def setUp(self) -> None:
        """Sets up the database mock and frontend test client."""
        super().setUp()
        self.frontend_blueprint = radar_frontend.create_frontend_blueprint(
            self.database)

        server = Flask(__name__)
        server.register_blueprint(self.frontend_blueprint)

        self.frontend_test_client = server.test_client().__enter__()  # type: ignore

    def tearDown(self) -> None:
        """Tears down the flask test client and database mock."""
        super().tearDown()
        self.frontend_test_client.__exit__(None, None, None)

    def test_index(self) -> None:
        """Snapshot tests the empty index page."""
        content = self.frontend_test_client.get('/')
        self.assertMatchSnapshot(content.data)

    def test_event_details(self) -> None:
        """Snapshot tests event details page for index 0.

        This entry should come from the database mock."""

        content = self.frontend_test_client.get('/event_details/0')

        self.assertMatchSnapshot(content.data)

    def test_client_info(self) -> None:
        """Snapshot client details page for the first session uuid.

        This entry should come from the database mock."""

        content = self.frontend_test_client.get(
            f'/client_info/{test_radar_common.TEST_SESSION_UUID}')

        self.assertMatchSnapshot(content.data)
