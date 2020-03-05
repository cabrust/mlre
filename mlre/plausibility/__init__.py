"""Plausibility: Plumbing for various plausibility checks."""
import typing

import grappa


class AssertionErrorHandler:
    """Captures and handles AssertionErrors."""

    def __enter__(self) -> None:
        self.old_trigger = grappa.Test._trigger  # pylint: disable=W0201
        grappa.Test._trigger =\
            lambda self_, trigger_=self.old_trigger: _replaced_trigger(
                self_, trigger_)  # pragma: no mutate

    def __exit__(self, exc_type: type, exc_val: typing.Any, exc_tb: typing.Any) -> None:
        grappa.Test._trigger = self.old_trigger


def _replaced_trigger(self: grappa.Test, trigger: typing.Callable) -> typing.Any:
    try:
        result = trigger(self)  # pragma: no mutate
        return result  # pragma: no mutate
    except AssertionError:
        pass
