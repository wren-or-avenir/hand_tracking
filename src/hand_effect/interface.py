from dataclasses import dataclass
from typing import Protocol, Sequence, TypeAlias


@dataclass(frozen=True)
class Point:
    x: float
    y: float


@dataclass(frozen=True)
class HandTips:
    thumb: Point
    index: Point
    middle: Point
    pinky: Point
    landmarks: tuple[Point, ...] = ()


Quad: TypeAlias = tuple[Point, Point, Point, Point]


class HandTracker(Protocol):
    def detect(self, frame: object) -> Sequence[HandTips]: ...
