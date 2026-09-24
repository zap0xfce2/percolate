"""Tests for percolate/models/farm.py."""

from __future__ import annotations

from percolate.models.farm import Farm
from percolate.models.plot import Plot


def _farm_with_planted(count: int, planted: set[int]) -> Farm:
    plots = [Plot() for _ in range(count)]
    for index in planted:
        plots[index].plant("arabica", growth_time=60.0, now=0.0)
    return Farm(plots=plots)


def test_next_empty_plot_skips_planted_neighbours():
    farm = _farm_with_planted(4, planted={0, 1})
    assert farm.next_empty_plot(after=0) == 2


def test_next_empty_plot_wraps_around():
    farm = _farm_with_planted(3, planted={1, 2})
    assert farm.next_empty_plot(after=2) == 0


def test_next_empty_plot_returns_none_when_all_planted():
    farm = _farm_with_planted(3, planted={0, 1, 2})
    assert farm.next_empty_plot(after=1) is None
