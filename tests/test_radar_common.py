"""Common data for unit tests."""
import typing
import uuid

from mlre.radar import radar_common

TEST_HOSTNAME: str = "test_hostname"
TEST_ENDPOINT: str = "https://api.test_url.org/"
TEST_SESSION_UUID: uuid.UUID = uuid.uuid1()
TEST_EVENT_SEVERITY: radar_common.Severity = radar_common.Severity.INFO
TEST_EVENT_DESCRIPTION: str = "This is a test event"
TEST_EVENT_LOCATION: str = __name__
TEST_EVENT_FREEZE_FRAME: radar_common.FreezeFrameData = {
    "test_data": 1.23456789}
TEST_EVENT_FREEZE_FRAME_ALTERNATIVE: radar_common.FreezeFrameData = {
    "test_data": 1.23456789}
TEST_ENVIRONMENT: typing.Dict[str, str] = {"ENV1": "env1_test", "ENV2": "ENV2"}

TEST_EVENT_IDENTIFIER: radar_common.EventIdentifier = radar_common.EventIdentifier(
    TEST_EVENT_SEVERITY, TEST_EVENT_LOCATION, TEST_EVENT_DESCRIPTION)
