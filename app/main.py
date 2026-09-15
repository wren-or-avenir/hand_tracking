import argparse
import logging
from pathlib import Path

from hand_effect.core import HandEffectPipeline
from hand_effect.mock import MockHandTracker


ROOT = Path(__file__).parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description='Hand-controlled corner-pin effect')
    parser.add_argument('--mock', action='store_true', help='run without a camera')
    parser.add_argument('--camera', type=int, default=0, help='camera device index')
    parser.add_argument('--confidence', type=float, default=0.5, help='MediaPipe confidence threshold')
    parser.add_argument('--opacity', type=float, default=0.65, help='effect opacity from 0 to 1')
    parser.add_argument('--min-area', type=float, default=0.002, help='minimum normalized quad area')
    args = parser.parse_args()
    if not 0 <= args.opacity <= 1:
        parser.error('--opacity must be between 0 and 1')
    logging.basicConfig(level=logging.INFO, format='[%(name)s] [%(levelname)s] %(message)s')

    if args.mock:
        pipeline = HandEffectPipeline(MockHandTracker(), args.min_area)
        for frame in range(3):
            result = pipeline.process(frame)
            logging.getLogger('pipeline').info(
                'frame=%d state=%s quads=%d', frame, result.state.value, len(result.quads)
            )
        return

    import cv2

    from hand_effect.runtime import MediaPipeHandTracker, draw_hands, render_effect

    model = ROOT / 'models' / 'hand_landmarker.task'
    if not model.exists():
        parser.error(f'missing MediaPipe model: {model}')

    tracker = MediaPipeHandTracker(model, args.confidence)
    camera = cv2.VideoCapture(args.camera)
    if not camera.isOpened():
        tracker.close()
        parser.error(f'cannot open camera {args.camera}')

    pipeline = HandEffectPipeline(tracker, args.min_area)
    logger = logging.getLogger('pipeline')
    previous_state = None
    window = 'Hand Tracking Corner Pin'
    try:
        cv2.namedWindow(window, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(window, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        while True:
            ok, frame = camera.read()
            if not ok:
                raise RuntimeError('camera stream ended')
            frame = cv2.flip(frame, 1)
            result = pipeline.process(frame)
            if result.state is not previous_state:
                logger.info('state=%s', result.state.value)
                previous_state = result.state
            display = render_effect(frame, result.quads, args.opacity)
            cv2.imshow(window, draw_hands(display, result.hands))
            if cv2.waitKey(1) & 0xFF in (27, ord('q')):
                break
    finally:
        tracker.close()
        camera.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
