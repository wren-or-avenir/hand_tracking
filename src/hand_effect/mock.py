from collections.abc import Sequence

from .interface import HandTips, Point


class MockHandTracker:
    def __init__(self) -> None:
        self.frame = 0

    def detect(self, frame: object) -> Sequence[HandTips]:
        self.frame += 1
        if self.frame == 1:
            return []
        return [
            HandTips(Point(0.20, 0.25), Point(0.24, 0.75)),
            HandTips(Point(0.80, 0.28), Point(0.76, 0.72)),
        ]
