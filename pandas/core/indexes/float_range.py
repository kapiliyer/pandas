from __future__ import annotations

import numpy as np


class float_range:
    """
    Modified Python built-in function range that accepts floats as arguments.

    Parameters
    ----------
    start : float (default: 0.0)
        If "stop" is not given, interpreted as "stop" instead.
    stop : float (default: None)
    step : float (default: 1.0)

    Attributes
    ----------
    start
    stop
    step
    current

    Methods
    ----------
    index
    """

    def __init__(self, start, stop=None, step=1.0):
        if stop is None:
            stop, start = start, 0.0
        self.start = start
        self.current = start - step
        self.stop = stop
        self.step = step

    def __contains__(self, key):
        epsilon = (key - self.start) % self.step
        return (
            # Imprecision checking: self.start less than or equal to key
            (self.start < key or np.isclose(self.start, key))
            # Imprecision checking: key strictly less than self.stop
            and (key < self.stop and not np.isclose(self.stop, key))
            # Imprecision checking: nx % x => 0
            and (np.isclose(epsilon, 0) or np.isclose(epsilon, self.step))
        )

    def __eq__(self, other):
        return (
            np.isclose(self.start, other.start)
            and np.isclose(self.stop, other.stop)
            and np.isclose(self.step, other.step)
        )

    def __getitem__(self, key):
        if isinstance(key, slice):
            epsilon = (self.stop - self.start) % self.step
            # Imprecision checking: nx % x => 0
            if not np.isclose(epsilon, self.stop) and not np.isclose(epsilon, 0):
                # Round self.stop such that (self.stop - self.start) % self.step == 0
                stop = (
                    self.stop + (self.step - epsilon)
                    if epsilon > 0
                    else self.stop + epsilon
                )
            else:
                stop = self.stop
            if slice.step is not None:
                if slice.step < 0:
                    stop = max(
                        self.start, self.start + (self.length + slice.stop) * self.step
                    )
                else:
                    stop = min(stop, self.start + self.step * slice.stop)
            if slice.start is not None:
                if slice.start < 0:
                    start = max(self.start, stop + slice.start * self.step)
                else:
                    start = min(stop, self.start + slice.start * self.step)
            else:
                start = self.start
            step = self.step if slice.step is None else self.step * slice.step
            return float_range(start, stop, step)
        if isinstance(key, int):
            if key >= 0:
                ith = self.start + key * self.step
            else:
                ith = self.start + (self.length + key) * self.step
            if ith in self:
                return ith
            raise IndexError("range object index out of range")
        raise TypeError("range indices must be integers or slices, not float")

    def __iter__(self):
        return self

    def __len__(self):
        return self.length

    def __next__(self):
        self.current += self.step
        # Imprecision checking: self.current strictly less than self.stop
        if self.current < self.stop and not np.isclose(self.current, self.stop):
            return self.current
        raise StopIteration

    def index(self, key) -> int:
        if key not in self:
            raise ValueError(f"{key} is not in range")
        return round((key - self.start) / self.step)

    @property
    def length(self) -> int:
        if self.stop > 0:
            lo, hi = self.start, self.stop
            step = self.step
        else:
            hi, lo = self.start, self.stop
            step = -self.step
        if lo >= hi:
            return 0
        estimate = (hi - lo) // step
        # Imprecision checking: estimate is either an underestimate or correct
        if not np.isclose(lo + estimate * step, hi):
            estimate += 1
        return int(estimate)
