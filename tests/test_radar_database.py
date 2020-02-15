"""Test for radar database component."""
import unittest

import test_radar_common
from mlre.radar import radar_database


class TestRadarDatabase(unittest.TestCase):
    """Test for radar database component."""

    def setUp(self) -> None:
        self.database: radar_database.RadarDatabase = radar_database.RadarDatabase()

    def test_initial_state(self) -> None:
        """Test if initial database state is empty."""
        self.assertEqual(0, len(self.database.event_identifiers))

    def test_insert_1(self) -> None:
        """Test if inserting one event works correctly.

        Test if:
          - The number of event identifiers equals one.
          - If the one event identifier is correct.
          - If the freeze frame data matches.
        """

        self.database.insert_event(
            test_radar_common.TEST_EVENT_IDENTIFIER, test_radar_common.TEST_EVENT_FREEZE_FRAME)

        self.assertEqual(1, len(self.database.event_identifiers))
        self.assertEqual(test_radar_common.TEST_EVENT_IDENTIFIER,
                         self.database.event_identifiers[0])

        # Test if the freeze frame data matches
        event = self.database.event(test_radar_common.TEST_EVENT_IDENTIFIER)
        self.assertEqual(1, len(event))

        self.assertEqual(test_radar_common.TEST_EVENT_FREEZE_FRAME, event[0])

    def test_insert_2_identical_events(self) -> None:
        """Test if inserting two identical events works correctly."""
        # Insert one event and test it
        self.test_insert_1()
        self.database.insert_event(
            test_radar_common.TEST_EVENT_IDENTIFIER, test_radar_common.TEST_EVENT_FREEZE_FRAME)
