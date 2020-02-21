"""Test for radar database component."""
import typing
import unittest

import test_radar_common
from mlre.radar import radar_common, radar_database


class TestRadarDatabase(unittest.TestCase):
    """Test for radar database component."""

    def setUp(self) -> None:
        self.database: radar_database.RadarDatabase = radar_database.RadarDatabase()

    def test_initial_state(self) -> None:
        """Test if initial database state is empty."""
        self.assertEqual(0, len(self.database.event_identifiers()))

    def test_insert_1(self) -> None:
        """Test if inserting one event works correctly.

        Test if:
          - The number of event identifiers equals one.
          - If the one event identifier is correct.
          - If the freeze frame data matches.
        """

        self.database.insert_event(
            test_radar_common.TEST_SESSION_UUID,
            test_radar_common.TEST_EVENT_IDENTIFIER,
            test_radar_common.TEST_EVENT_FREEZE_FRAME)

        self.assertEqual(1, len(self.database.event_identifiers()))
        self.assertEqual(test_radar_common.TEST_EVENT_IDENTIFIER,
                         self.database.event_identifiers()[0])

        # Test if the freeze frame data matches
        event = self.database.event(test_radar_common.TEST_EVENT_IDENTIFIER)
        self.assertEqual(1, len(event))

        self.assertEqual((test_radar_common.TEST_SESSION_UUID,
                          test_radar_common.TEST_EVENT_FREEZE_FRAME), event[0])

    def test_insert_2_identical_events(self) -> None:
        """Test if inserting two identical events works correctly.

        Test if:
         - Inserting the first element works correctly.

        Test if after inserting the second element:
         - The number of event identifiers is still one.
         - If the one event identifier is correct.
         - If the freeze frame data matches and is in the correct order.
        """

        # Insert one event and test it
        self.test_insert_1()
        self.database.insert_event(
            test_radar_common.TEST_SESSION_UUID,
            test_radar_common.TEST_EVENT_IDENTIFIER,
            test_radar_common.TEST_EVENT_FREEZE_FRAME_ALTERNATIVE)

        self.assertEqual(1, len(self.database.event_identifiers()))
        self.assertEqual(test_radar_common.TEST_EVENT_IDENTIFIER,
                         self.database.event_identifiers()[0])

        # Test if the new freeze frame data matches.
        event = self.database.event(test_radar_common.TEST_EVENT_IDENTIFIER)
        self.assertEqual(2, len(event))

        # The sequence should be kept and the data should be identical.
        self.assertEqual((test_radar_common.TEST_SESSION_UUID,
                          test_radar_common.TEST_EVENT_FREEZE_FRAME), event[0])
        self.assertEqual(
            (test_radar_common.TEST_SESSION_UUID,
             test_radar_common.TEST_EVENT_FREEZE_FRAME_ALTERNATIVE), event[1])

    def test_insert_2_different_events(self) -> None:
        """Test if inserting two different events works correctly.

        Test if:
         - Inserting the first element works correctly.

        Test if after inserting the second element:
         - The number of event identifiers is two.
         - If both event identifiers are correct.
         - If the freeze frame data matches for both.
        """

        # Insert one event and test it
        self.test_insert_1()

        self.database.insert_event(
            test_radar_common.TEST_SESSION_UUID_ALTERNATIVE,
            test_radar_common.TEST_EVENT_IDENTIFIER_ALTERNATIVE,
            test_radar_common.TEST_EVENT_FREEZE_FRAME_ALTERNATIVE)

        self.assertEqual(2, len(self.database.event_identifiers()))
        event_identifiers: typing.List[radar_common.EventIdentifier] = [
            test_radar_common.TEST_EVENT_IDENTIFIER,
            test_radar_common.TEST_EVENT_IDENTIFIER_ALTERNATIVE]
        self.assertEqual(event_identifiers,
                         self.database.event_identifiers())

        # Test if the new freeze frame data matches.
        event1 = self.database.event(test_radar_common.TEST_EVENT_IDENTIFIER)
        event2 = self.database.event(
            test_radar_common.TEST_EVENT_IDENTIFIER_ALTERNATIVE)

        self.assertEqual(1, len(event1))
        self.assertEqual(1, len(event2))

        # The sequence should be kept and the data should be identical.
        self.assertEqual(
            (test_radar_common.TEST_SESSION_UUID,
             test_radar_common.TEST_EVENT_FREEZE_FRAME), event1[0])
        self.assertEqual(
            (test_radar_common.TEST_SESSION_UUID_ALTERNATIVE,
             test_radar_common.TEST_EVENT_FREEZE_FRAME_ALTERNATIVE), event2[0])

    def test_insert_1_client_info(self) -> None:
        """Tests if inserting client information works."""
        self.database.insert_client_info(test_radar_common.TEST_SESSION_UUID,
                                         test_radar_common.TEST_CLIENT_INFO)

        # Get the info back from the database
        actual_client_info = self.database.client_info(
            test_radar_common.TEST_SESSION_UUID)

        # Check for correctness
        self.assertEqual(test_radar_common.TEST_CLIENT_INFO,
                         actual_client_info,
                         "Client information for test session UUID should be correct.")

    def test_insert_2_different_client_infos(self) -> None:
        """Tests if inserting client infos for two sessions works."""
        self.database.insert_client_info(test_radar_common.TEST_SESSION_UUID_ALTERNATIVE,
                                         test_radar_common.TEST_CLIENT_INFO_ALTERNATIVE)

        self.test_insert_1_client_info()

        # Get the second info back from the database
        actual_client_info =\
            self.database.client_info(
                test_radar_common.TEST_SESSION_UUID_ALTERNATIVE)

        # Check for correctness
        self.assertEqual(test_radar_common.TEST_CLIENT_INFO_ALTERNATIVE,
                         actual_client_info,
                         "Client information for second test session UUID should be correct.")

    def test_insert_2_identical_client_infos(self) -> None:
        """Tests if inserting the same client info twice works.

        This should not fail, but rather just replace the client info."""

        self.test_insert_1_client_info()

        # Use the same UUID, but different info
        self.database.insert_client_info(test_radar_common.TEST_SESSION_UUID,
                                         test_radar_common.TEST_CLIENT_INFO_ALTERNATIVE)

        # Get the second info back from the database
        actual_client_info = self.database.client_info(
            test_radar_common.TEST_SESSION_UUID)

        # Check for correctness
        self.assertEqual(test_radar_common.TEST_CLIENT_INFO_ALTERNATIVE,
                         actual_client_info,
                         "Client information for first test session UUID should be overwritten.")
