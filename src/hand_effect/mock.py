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
            HandTips(
                Point(0.20, 0.65), Point(0.18, 0.25), Point(0.24, 0.20),
                Point(0.34, 0.35),
            ),
            HandTips(
                Point(0.80, 0.65), Point(0.82, 0.25), Point(0.76, 0.20),
                Point(0.66, 0.35),
            ),
        ]
