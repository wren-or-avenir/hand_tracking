import sys
from dataclasses import replace
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parents[1] / 'src'))

from hand_effect.core import HandEffectPipeline, State, quads_from_hands
from hand_effect.interface import HandTips, Point
from hand_effect.mock import MockHandTracker
from hand_effect.runtime import draw_hands, render_effect


def make_hand(x: float) -> HandTips:
    return HandTips(*(Point(x, y) for y in (0.1, 0.35, 0.65, 0.9)))


def test_quad_mapping() -> None:
    hands = [make_hand(0.8), make_hand(0.2)]
    quads = quads_from_hands(hands)
    assert len(quads) == 3
    assert quads[0] == (
        Point(0.2, 0.1), Point(0.8, 0.1), Point(0.8, 0.35), Point(0.2, 0.35)
    )
    assert quads_from_hands(hands[:1]) == ()
    assert quads_from_hands([replace(hands[0], pinky=Point(1.1, 0.9)), hands[1]]) == ()
    flat = HandTips(*(Point(0.2, 0.1) for _ in range(4)))
    assert not any(quads_from_hands([flat, replace(flat, thumb=Point(0.8, 0.1))]))


def test_render_effects_stay_inside_quads() -> None:
    frame = np.zeros((100, 100, 3), np.uint8)
    frame[..., 0] = np.arange(100, dtype=np.uint8)
    output = render_effect(frame, quads_from_hands([make_hand(0.2), make_hand(0.8)]), opacity=1)
    assert np.array_equal(output[20, 50], 255 - frame[20, 50])
    assert len({tuple(output[y, 50]) for y in (20, 50, 77)}) == 3
    assert np.array_equal(output[0, 0], frame[0, 0])


def test_draw_hands() -> None:
    frame = np.zeros((100, 100, 3), np.uint8)
    landmarks = tuple(Point(index / 20, index / 20) for index in range(21))
    output = draw_hands(frame, (replace(make_hand(0.2), landmarks=landmarks),))
    assert output[..., 1].any()
    assert output[..., 2].any()
    assert not frame.any()


def test_pipeline_states() -> None:
    pipeline = HandEffectPipeline(MockHandTracker())
    assert pipeline.process(None).state is State.WAITING
    result = pipeline.process(None)
    assert result.state is State.TRACKING
    assert len(result.quads) == 3


if __name__ == '__main__':
    test_quad_mapping()
    test_pipeline_states()
    test_render_effects_stay_inside_quads()
    test_draw_hands()
    print('pipeline checks passed')
