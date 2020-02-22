"""Radar frontend component."""
from flask import Blueprint

from mlre.radar import radar_database


def create_frontend_blueprint(database: radar_database.RadarDatabase) -> Blueprint:  # pylint: disable=W0613
    """Creates the frontend blueprint."""
    frontend = Blueprint(__name__, __name__)

    return frontend
