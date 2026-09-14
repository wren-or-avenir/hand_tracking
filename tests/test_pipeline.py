import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from hand_effect.core import HandEffectPipeline, State, quad_from_hands
from hand_effect.interface import HandTips, Point
from hand_effect.mock import MockHandTracker


def test_quad_mapping() -> None:
    hands = [
        HandTips(Point(0.8, 0.8), Point(0.7, 0.2)),
        HandTips(Point(0.2, 0.7), Point(0.3, 0.3)),
    ]
    assert quad_from_hands(hands) == (
        Point(0.3, 0.3), Point(0.7, 0.2), Point(0.8, 0.8), Point(0.2, 0.7)
    )
    assert quad_from_hands(hands[:1]) is None
    assert quad_from_hands([hands[0], HandTips(Point(1.1, 0.2), Point(0.8, 0.8))]) is None
    assert quad_from_hands([HandTips(Point(0.1, 0.1), Point(0.2, 0.1)), HandTips(Point(0.3, 0.1), Point(0.4, 0.1))]) is None


def test_pipeline_states() -> None:
    pipeline = HandEffectPipeline(MockHandTracker())
    assert pipeline.process(None).state is State.WAITING
    assert pipeline.process(None).state is State.TRACKING


if __name__ == "__main__":
    test_quad_mapping()
    test_pipeline_states()
    print("pipeline checks passed")
