"""Server component for the radar API."""
import typing

from flask import Flask, jsonify

import mlre
from mlre.radar import radar_database


def create_api_server(database: radar_database.RadarDatabase,   # type: ignore  # pylint: disable=W0613
                      configuration: typing.Optional[typing.Mapping[str, typing.Any]] = None)\
        -> Flask:
    """Creates an instance of the API server.

    Args:
        database: An instance of the radar event and client info database.
        configuration: Optional flask configuration values.
    """
    api_server = Flask(
        __name__, instance_relative_config=True)  # pragma: no mutate

    # Apply configuration if possible
    if configuration is not None:  # type: ignore
        api_server.config.from_mapping(configuration)  # type: ignore

    @api_server.route('/version')
    def get_api_version() -> str:  # type: ignore  # pylint: disable=W0612
        """Give api server and mlre versions."""
        return jsonify({'api': '1', 'mlre': mlre.__version__})  # type: ignore

    return api_server


__all__ = ["create_api_server"]
