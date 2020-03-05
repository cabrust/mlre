"""Tests the AssertionError handler."""
import unittest

import grappa
from mlre import plausibility


class TestPlausibilityAssertionHandler(unittest.TestCase):
    """Tests the AssertionError handler."""

    def test_assertion_in_context(self) -> None:  # pylint: disable=R0201
        """An AssertionError raised in the context should do nothing."""
        with plausibility.AssertionErrorHandler():
            1 | grappa.should.be.equal.to(
                0, msg="This error should be captured by the context.")

    def test_value_error_always(self) -> None:
        """A ValueError should always be raised."""
        with self.assertRaises(ValueError):
            with plausibility.AssertionErrorHandler():
                raise ValueError()

        with self.assertRaises(ValueError):
            raise ValueError()

    def test_assertion_out_of_context(self) -> None:
        """An AssertionError raised outside of the context should by raised."""
        with self.assertRaises(AssertionError):
            1 | grappa.should.be.equal.to(
                0, msg="This error should not be handled by the context!")

        # Build and tear down the context using the in-context test
        self.test_assertion_in_context()

        with self.assertRaises(AssertionError):
            1 | grappa.should.be.equal.to(
                0, msg="This error should also not be handled by the context!")

    def test_nested_handlers(self) -> None:
        """Nested AssertionErrorHandlers should still perform as expected."""
        with plausibility.AssertionErrorHandler():
            1 | grappa.should.be.equal.to(
                0, msg="This error should be captured by the context.")
            with plausibility.AssertionErrorHandler():
                1 | grappa.should.be.equal.to(
                    0, msg="This error should be captured by the context.")
            1 | grappa.should.be.equal.to(
                0, msg="This error should be captured by the context.")

        with self.assertRaises(AssertionError):
            1 | grappa.should.be.equal.to(
                0, msg="This error should not be handled by the context!")
