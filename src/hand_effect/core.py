from dataclasses import dataclass
from enum import Enum

from .interface import HandTips, HandTracker, Quad


class State(str, Enum):
    WAITING = 'waiting'
    TRACKING = 'tracking'


@dataclass(frozen=True)
class Result:
    state: State
    quads: tuple[Quad | None, ...]
    hands: tuple[HandTips, ...]


def quads_from_hands(hands: list[HandTips], min_area: float = 0.002) -> tuple[Quad | None, ...]:
    if len(hands) != 2:
        return ()

    tips = [
        (hand.thumb, hand.index, hand.middle, hand.pinky)
        for hand in hands
    ]
    if any(not 0 <= value <= 1 for hand in tips for point in hand for value in (point.x, point.y)):
        return ()

    left, right = sorted(tips, key=lambda hand: sum(point.x for point in hand) / len(hand))
    quads = []
    for index in range(3):
        quad = (left[index], right[index], right[index + 1], left[index + 1])
        area = abs(sum(
            point.x * quad[(corner + 1) % 4].y - quad[(corner + 1) % 4].x * point.y
            for corner, point in enumerate(quad)
        )) / 2
        quads.append(quad if area >= min_area else None)
    return tuple(quads)


class HandEffectPipeline:
    def __init__(self, tracker: HandTracker, min_area: float = 0.002) -> None:
        self.tracker = tracker
        self.min_area = min_area
        self.state = State.WAITING

    def process(self, frame: object) -> Result:
        hands = tuple(self.tracker.detect(frame))
        quads = quads_from_hands(list(hands), self.min_area)
        self.state = State.TRACKING if any(quads) else State.WAITING
        return Result(self.state, quads, hands)
