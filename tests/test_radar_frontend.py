"""Tests for the radar frontend component."""
import unittest

from flask import Flask

import test_radar_common
from mlre.radar import radar_frontend


class RadarFrontendTestCase(test_radar_common.MockedDatabaseTestCase):
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
