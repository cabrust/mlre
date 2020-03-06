"""Test for radar database component."""
import os
import typing
import unittest

import test_radar_common
from mlre.radar import radar_common, radar_database


class TestRadarDatabase(unittest.TestCase):
    """Test for radar database component."""

    def setUp(self) -> None:
        # Clean up temp files for this fixture
        if os.path.exists(test_radar_common.TEST_DATABASE_FILENAME_1):
            os.remove(test_radar_common.TEST_DATABASE_FILENAME_1)
        if os.path.exists(test_radar_common.TEST_DATABASE_FILENAME_2):
            os.remove(test_radar_common.TEST_DATABASE_FILENAME_2)

        self.database: radar_database.RadarDatabase = radar_database.RadarDatabase()

    def test_initial_state(self) -> None:
        """Test if initial database state is empty."""
        self.assertEqual(0, len(self.database.event_identifiers()))

    def test_persistent_db_save_and_load(self) -> None:
        """Test if database information is persistent."""
        self.database.insert_client_info(test_radar_common.TEST_SESSION_UUID,
                                         test_radar_common.TEST_CLIENT_INFO)

        index_1 = self.database.insert_event(
            test_radar_common.TEST_SESSION_UUID,
            test_radar_common.TEST_EVENT_IDENTIFIER,
            test_radar_common.TEST_EVENT_FREEZE_FRAME)

        # Save and reload the data from an empty db
        self.database.save(test_radar_common.TEST_DATABASE_FILENAME_1)
        self.database = radar_database.RadarDatabase()
        self.database.load(test_radar_common.TEST_DATABASE_FILENAME_1)

        # Get the info back from the database
        actual_client_info = self.database.client_info(
            test_radar_common.TEST_SESSION_UUID)

        # Check for correctness
        self.assertEqual(test_radar_common.TEST_CLIENT_INFO,
                         actual_client_info,
                         "Client information for test session UUID should be correct.")

        self._check_event_data(index_1)

    def _check_event_data(self, index_1: int) -> None:
        self.assertEqual(1, len(self.database.event_identifiers()))
        self.assertEqual((index_1, test_radar_common.TEST_EVENT_IDENTIFIER),
                         self.database.event_identifiers()[0])
        # Test if the freeze frame data matches
        event = self.database.event(index_1)
        self.assertEqual(1, len(event[1]))
        self.assertEqual((test_radar_common.TEST_SESSION_UUID,
                          test_radar_common.TEST_EVENT_FREEZE_FRAME), event[1][0])

    def test_load_tests_for_empty_db_event(self) -> None:
        """Test if the load function actually performs an emptiness check."""

        # Make sure the file exists somewhere
        self.database.save(test_radar_common.TEST_DATABASE_FILENAME_1)

        # Write things into the database
        self.test_insert_1()

        with self.assertRaises(ValueError) as error:
            self.database.load(test_radar_common.TEST_DATABASE_FILENAME_1)

        self.assertEqual("The database is not empty. Cannot load!",
                         error.exception.args[0])  # type: ignore

    def test_load_tests_for_empty_db_client_info(self) -> None:
        """Test if the load function actually performs an emptiness check."""

        # Make sure the file exists somewhere
        empty_db = radar_database.RadarDatabase()
        empty_db.save(test_radar_common.TEST_DATABASE_FILENAME_1)

        # Write things into the database
        self.test_insert_1_client_info()

        with self.assertRaises(ValueError) as error:
            self.database.load(test_radar_common.TEST_DATABASE_FILENAME_1)

        self.assertEqual("The database is not empty. Cannot load!",
                         error.exception.args[0])  # type: ignore

    def test_insert_1(self) -> int:
        """Test if inserting one event works correctly.

        Test if:
          - The number of event identifiers equals one.
          - If the one event identifier is correct.
          - If the freeze frame data matches.
        """

        index_1 = self.database.insert_event(
            test_radar_common.TEST_SESSION_UUID,
            test_radar_common.TEST_EVENT_IDENTIFIER,
            test_radar_common.TEST_EVENT_FREEZE_FRAME)

        self._check_event_data(index_1)

        return index_1

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
        index_1 = self.test_insert_1()
        index_2: int = self.database.insert_event(
            test_radar_common.TEST_SESSION_UUID,
            test_radar_common.TEST_EVENT_IDENTIFIER,
            test_radar_common.TEST_EVENT_FREEZE_FRAME_ALTERNATIVE)

        self.assertEqual(1, len(self.database.event_identifiers()))
        self.assertEqual((index_1, test_radar_common.TEST_EVENT_IDENTIFIER),
                         self.database.event_identifiers()[0])

        # Test if the new freeze frame data matches.
        event = self.database.event(index_2)
        self.assertEqual(2, len(event[1]))

        # The sequence should be kept and the data should be identical.
        self.assertEqual((test_radar_common.TEST_SESSION_UUID,
                          test_radar_common.TEST_EVENT_FREEZE_FRAME), event[1][0])
        self.assertEqual(
            (test_radar_common.TEST_SESSION_UUID,
             test_radar_common.TEST_EVENT_FREEZE_FRAME_ALTERNATIVE), event[1][1])

        # The indices should be identical
        self.assertEqual(
            index_1, index_2, "The indices of identical events should be identical.")

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
        index_1 = self.test_insert_1()

        index_2: int = self.database.insert_event(
            test_radar_common.TEST_SESSION_UUID_ALTERNATIVE,
            test_radar_common.TEST_EVENT_IDENTIFIER_ALTERNATIVE,
            test_radar_common.TEST_EVENT_FREEZE_FRAME_ALTERNATIVE)

        self.assertEqual(2, len(self.database.event_identifiers()))
        event_identifiers: typing.List[typing.Tuple[int, radar_common.EventIdentifier]] = [
            (index_1, test_radar_common.TEST_EVENT_IDENTIFIER),
            (index_2, test_radar_common.TEST_EVENT_IDENTIFIER_ALTERNATIVE)]
        self.assertEqual(event_identifiers,
                         self.database.event_identifiers())

        # Test if the new freeze frame data matches.
        event1 = self.database.event(index_1)
        event2 = self.database.event(index_2)

        self.assertEqual(1, len(event1[1]))
        self.assertEqual(1, len(event2[1]))

        # The sequence should be kept and the data should be identical.
        self.assertEqual(
            (test_radar_common.TEST_SESSION_UUID,
             test_radar_common.TEST_EVENT_FREEZE_FRAME), event1[1][0])
        self.assertEqual(
            (test_radar_common.TEST_SESSION_UUID_ALTERNATIVE,
             test_radar_common.TEST_EVENT_FREEZE_FRAME_ALTERNATIVE), event2[1][0])

        # The indices should be different
        self.assertNotEqual(
            index_1, index_2, "The indices of different events should be different.")

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
