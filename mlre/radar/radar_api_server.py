"""Server component for the radar API."""
import typing
import uuid

from flask import Flask, request

import mlre
from mlre.radar import radar_common, radar_database


def create_api_server(database: radar_database.RadarDatabase,   # type: ignore
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

    @api_server.route('/version')  # type: ignore
    def get_version() -> typing.Dict[str, str]:  # pylint: disable=W0612
        """Give api server and mlre versions."""
        return {'api': '1', 'mlre': mlre.__version__}

    @api_server.route('/report_event', methods=['POST'])  # type: ignore
    def report_event() -> str:  # pylint: disable=W0612
        # Decode request
        request_json = request.json  # type: ignore
        session_id: uuid.UUID = uuid.UUID(
            request_json['session_id'])  # type: ignore
        event_identifier: radar_common.EventIdentifier =\
            radar_common.EventIdentifier(
                *request_json['event_identifier'])  # type: ignore

        freeze_frame: radar_common.FreezeFrameData =\
            request_json['freeze_frame']  # type: ignore

        # Make database call
        database.insert_event(session_id, event_identifier, freeze_frame)
        return ''

    return api_server


__all__ = ["create_api_server"]
