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

    def test_empty_index(self) -> None:
        """Snapshot tests the empty index page."""
        empty_index = self.frontend_test_client.get('/')
        self.assertMatchSnapshot(empty_index.data)
