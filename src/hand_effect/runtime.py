import time
from pathlib import Path

import cv2
import mediapipe as mp
import numpy as np

from .interface import HandTips, Point, Quad


class MediaPipeHandTracker:
    def __init__(self, model: Path, confidence: float = 0.5) -> None:
        options = mp.tasks.vision.HandLandmarkerOptions(
            base_options=mp.tasks.BaseOptions(model_asset_path=str(model)),
            running_mode=mp.tasks.vision.RunningMode.VIDEO,
            num_hands=2,
            min_hand_detection_confidence=confidence,
            min_hand_presence_confidence=confidence,
            min_tracking_confidence=confidence,
        )
        self.landmarker = mp.tasks.vision.HandLandmarker.create_from_options(options)
        self.timestamp = 0

    def detect(self, frame: object) -> list[HandTips]:
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        self.timestamp = max(self.timestamp + 1, time.monotonic_ns() // 1_000_000)
        result = self.landmarker.detect_for_video(image, self.timestamp)
        hands = []
        for hand in result.hand_landmarks:
            landmarks = tuple(Point(point.x, point.y) for point in hand)
            hands.append(HandTips(
                landmarks[4], landmarks[8], landmarks[12], landmarks[20], landmarks
            ))
        return hands

    def close(self) -> None:
        self.landmarker.close()


def _effects(frame: np.ndarray) -> tuple[np.ndarray, ...]:
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    inverted = cv2.bitwise_not(frame)
    neon = cv2.applyColorMap(gray, cv2.COLORMAP_TURBO)
    comic = cv2.applyColorMap((gray // 64) * 64, cv2.COLORMAP_MAGMA)
    comic[cv2.Canny(gray, 60, 140) != 0] = 0
    return inverted, neon, comic


def draw_hands(frame: np.ndarray, hands: tuple[HandTips, ...]) -> np.ndarray:
    height, width = frame.shape[:2]
    output = frame.copy()
    for hand in hands:
        if len(hand.landmarks) != 21:
            continue
        points = tuple(
            (round(point.x * (width - 1)), round(point.y * (height - 1)))
            for point in hand.landmarks
        )
        for connection in mp.tasks.vision.HandLandmarksConnections.HAND_CONNECTIONS:
            cv2.line(output, points[connection.start], points[connection.end], (0, 255, 0), 2)
        for point in points:
            cv2.circle(output, point, 3, (0, 0, 255), -1)
    return output


def render_effect(
    frame: np.ndarray,
    quads: tuple[Quad | None, ...],
    opacity: float = 0.65,
) -> np.ndarray:
    if not quads:
        return frame

    height, width = frame.shape[:2]
    output = frame.copy()
    for quad, effect in zip(quads, _effects(frame)):
        if quad is None:
            continue
        destination = np.int32(tuple(
            (point.x * (width - 1), point.y * (height - 1))
            for point in quad
        ))
        mask = np.zeros((height, width), np.uint8)
        cv2.fillConvexPoly(mask, destination, 255)
        blended = cv2.addWeighted(output, 1 - opacity, effect, opacity, 0)
        output[mask != 0] = blended[mask != 0]
    return output
