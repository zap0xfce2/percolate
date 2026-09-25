"""Tests for percolate/models/farm.py."""

from __future__ import annotations

from percolate.models.farm import Farm
from percolate.models.plot import Plot


def _farm_with_planted(count: int, planted: set[int]) -> Farm:
    plots = [Plot() for _ in range(count)]
    for index in planted:
        plots[index].plant("arabica", growth_time=60.0, now=0.0)
    return Farm(plots=plots)


def _is_empty(plot: Plot) -> bool:
    return plot.is_empty


def test_nearest_plot_skips_non_matching_neighbours():
    farm = _farm_with_planted(4, planted={0, 1})
    assert farm.nearest_plot(after=0, matches=_is_empty) == 2


def test_nearest_plot_prefers_right_over_left():
    farm = _farm_with_planted(3, planted={1})
    assert farm.nearest_plot(after=1, matches=_is_empty) == 2


def test_nearest_plot_falls_back_to_nearest_left():
    farm = _farm_with_planted(4, planted={2, 3})
    assert farm.nearest_plot(after=3, matches=_is_empty) == 1


def test_nearest_plot_returns_none_when_nothing_matches():
    farm = _farm_with_planted(3, planted={0, 1, 2})
    assert farm.nearest_plot(after=1, matches=_is_empty) is None


def test_nearest_plot_ignores_the_starting_plot():
    farm = _farm_with_planted(2, planted={1})
    assert farm.nearest_plot(after=0, matches=_is_empty) is None
