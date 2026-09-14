import argparse
import logging

from hand_effect.core import HandEffectPipeline
from hand_effect.mock import MockHandTracker


def main() -> None:
    parser = argparse.ArgumentParser(description="Hand-controlled corner-pin effect")
    parser.add_argument("--mock", action="store_true", help="run without a camera")
    parser.add_argument("--min-area", type=float, default=0.002, help="minimum normalized quad area")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="[%(name)s] [%(levelname)s] %(message)s")

    if not args.mock:
        parser.error("camera adapter is added in phase 2; run with --mock for now")

    pipeline = HandEffectPipeline(MockHandTracker(), args.min_area)
    for frame in range(3):
        result = pipeline.process(frame)
        logging.getLogger("pipeline").info("frame=%d state=%s quad=%s", frame, result.state.value, result.quad)


if __name__ == "__main__":
    main()
