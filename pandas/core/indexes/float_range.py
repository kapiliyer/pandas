from __future__ import annotations

import numpy as np


class float_range:
    """
    Modified Python built-in function range that accepts floats as arguments.

    Parameters
    ----------
    start : float (default: 0.0)
        If "stop" is not given, interpreted as "stop" instead.
    stop : float (default: 0.0)
    step : float (default: 1.0)

    Attributes
    ----------
    start
    stop
    step
    current
    """

    def __init__(self, start=0.0, stop=0.0, step=1.0):
        if stop is None:
            stop, start = start, 0.0
        self.start = start
        self.current = start - step
        self.stop = stop
        self.step = step

    def __contains__(self, key):
        closeness_to_range = (key - self.start) % self.step
        return (
            (self.start < key or np.isclose(self.start, key))
            and (key < self.stop and not np.isclose(self.stop, key))
            and (
                np.isclose(closeness_to_range, 0)
                or np.isclose(closeness_to_range, self.step)
            )
        )

    def __eq__(self, other):
        return (
            np.isclose(self.start, other.start)
            and np.isclose(self.stop, other.stop)
            and np.isclose(self.step, other.step)
        )

    def __getitem__(self, key):
        # Allows for reversing
        if isinstance(key, slice):
            if key.start is None and key.stop is None and key.step == -1:
                return float_range(
                    start=self.start + (len(self) - 1) * self.step,
                    stop=self.start - self.step,
                    step=-self.step,
                )
            raise IndexError
        raise TypeError

    def __iter__(self):
        return self

    def __len__(self):
        return self.length

    def __next__(self):
        self.current += self.step
        if self.current < self.stop and not np.isclose(self.current, self.stop):
            return self.current
        raise StopIteration

    def index(self, key) -> int:
        if key not in self:
            raise ValueError
        return round((key - self.start) / self.step)

    @property
    def length(self) -> int:
        estimate = (self.stop - self.start) // self.step
        if not np.isclose(self.start + estimate * self.step, self.stop):
            estimate += 1
        return estimate
