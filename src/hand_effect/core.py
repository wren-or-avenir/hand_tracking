from dataclasses import dataclass
from enum import Enum

from .interface import HandTips, HandTracker, Point, Quad


class State(str, Enum):
    WAITING = "waiting"
    TRACKING = "tracking"


@dataclass(frozen=True)
class Result:
    state: State
    quad: Quad | None


def quad_from_hands(hands: list[HandTips], min_area: float = 0.002) -> Quad | None:
    if len(hands) != 2 or any(not 0 <= value <= 1 for hand in hands for point in (hand.thumb, hand.index) for value in (point.x, point.y)):
        return None

    left, right = sorted(hands, key=lambda hand: (hand.thumb.x + hand.index.x) / 2)
    left_top, left_bottom = sorted((left.thumb, left.index), key=lambda point: point.y)
    right_top, right_bottom = sorted((right.thumb, right.index), key=lambda point: point.y)
    quad = (left_top, right_top, right_bottom, left_bottom)
    area = abs(sum(point.x * quad[(index + 1) % 4].y - quad[(index + 1) % 4].x * point.y for index, point in enumerate(quad))) / 2
    return quad if area >= min_area else None


class HandEffectPipeline:
    def __init__(self, tracker: HandTracker, min_area: float = 0.002) -> None:
        self.tracker = tracker
        self.min_area = min_area
        self.state = State.WAITING

    def process(self, frame: object) -> Result:
        quad = quad_from_hands(list(self.tracker.detect(frame)), self.min_area)
        self.state = State.TRACKING if quad else State.WAITING
        return Result(self.state, quad)
