"""Common data for unit tests."""
import typing
import uuid

from mlre.radar import radar_common

TEST_ENDPOINT: str = "https://api.test_url.org/"

TEST_HOSTNAME: str = "test_hostname"
TEST_HOSTNAME_ALTERNATIVE: str = "test_hostname2"

TEST_ENVIRONMENT: typing.Dict[str, str] = {"ENV1": "env1_test", "ENV2": "ENV2"}
TEST_ENVIRONMENT_ALTERNATIVE: typing.Dict[str, str] = {
    "ENV1": "env1_test1", "ENV2": "ENV212"}

TEST_CLIENT_INFO = radar_common.ClientInfo(TEST_HOSTNAME, TEST_ENVIRONMENT)
TEST_CLIENT_INFO_ALTERNATIVE = radar_common.ClientInfo(TEST_HOSTNAME_ALTERNATIVE,
                                                       TEST_ENVIRONMENT_ALTERNATIVE)

TEST_SESSION_UUID: uuid.UUID = uuid.uuid1()
TEST_SESSION_UUID_ALTERNATIVE: uuid.UUID = uuid.uuid4()

TEST_EVENT_SEVERITY: radar_common.Severity = radar_common.Severity.INFO
TEST_EVENT_DESCRIPTION: str = "This is a test event"
TEST_EVENT_DESCRIPTION_ALTERNATIVE: str = "This is another test event"
TEST_EVENT_LOCATION: str = __name__
TEST_EVENT_FREEZE_FRAME: radar_common.FreezeFrameData = {
    "test_data": 1.23456789}
TEST_EVENT_FREEZE_FRAME_ALTERNATIVE: radar_common.FreezeFrameData = {
    "test_data": 1.23456789}

TEST_EVENT_IDENTIFIER: radar_common.EventIdentifier = radar_common.EventIdentifier(
    TEST_EVENT_SEVERITY, TEST_EVENT_LOCATION, TEST_EVENT_DESCRIPTION)

TEST_EVENT_IDENTIFIER_ALTERNATIVE: radar_common.EventIdentifier = radar_common.EventIdentifier(
    TEST_EVENT_SEVERITY, TEST_EVENT_LOCATION, TEST_EVENT_DESCRIPTION_ALTERNATIVE)
