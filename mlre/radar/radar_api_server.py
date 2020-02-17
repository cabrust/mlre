"""Server component for the radar API."""
import typing

from flask import Flask

from mlre.radar import radar_database


def create_api_server(database: radar_database.RadarDatabase,   # type: ignore
                      configuration: typing.Optional[typing.Mapping[str, typing.Any]] = None) -> Flask:
    api_server = Flask(
        __name__, instance_relative_config=True)  # pragma: no mutate

    # Apply configuration if possible
    if configuration is not None:  # type: ignore
        api_server.config.from_mapping(configuration)  # type: ignore

    return api_server


__all__ = ["create_api_server"]
