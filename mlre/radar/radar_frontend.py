"""Radar frontend component."""
import typing

from flask import Blueprint, render_template

from mlre.radar import radar_common, radar_database


def create_frontend_blueprint(database: radar_database.RadarDatabase) -> Blueprint:  # pylint: disable=W0613
    """Creates the frontend blueprint."""
    frontend = Blueprint(__name__, __name__, template_folder='templates')

    @frontend.route('/')  # type: ignore
    # type: ignore
    # pylint: disable=W0612
    def index() -> typing.Any:
        event_identifiers = database.event_identifiers()

        context_data = [{
            "index": event_index,
            "severity": radar_common.Severity(event_identifier.severity),
            "location": event_identifier.location,
            "description": event_identifier.description,
            "frequency": len(database.event(event_index)[1])
        } for (event_index, event_identifier) in event_identifiers]

        return render_template('index.html', events=context_data)

    @frontend.route('/event_details/<event_index>')  # type: ignore
    # type: ignore
    # pylint: disable=W0612
    def event_details(event_index: int) -> typing.Any:
        event_identifier, freeze_frames = database.event(int(event_index))
        context_data = {
            "severity": radar_common.Severity(event_identifier.severity),
            "location": event_identifier.location,
            "description": event_identifier.description
        }

        return render_template('event_details.html',
                               event_identifier=context_data,
                               freeze_frames=freeze_frames)

    return frontend
