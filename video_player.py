from typing import Optional, Callable
import cv2
import numpy as np
from config import PLAYBACK_FPS
from logger import Logger


class VideoPlayer:
    def __init__(self, logger: Logger) -> None:
        self._cap: Optional[cv2.VideoCapture] = None
        self._total_frames: int = 0
        self._logger = logger

    def open(self, path: str) -> None:
        self._cap = cv2.VideoCapture(path)
        if not self._cap.isOpened():
            raise IOError(f"Could not open video: {path}")
        self._total_frames = int(self._cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self._logger.log(f"Opened video: {path} ({self._total_frames} frames)")

    @property
    def total_frames(self) -> int:
        return self._total_frames

    def is_valid_frame(self, frame_number: int) -> bool:
        return 0 <= frame_number < self._total_frames

    def read_frame(self, frame_number: int) -> Optional[np.ndarray]:
        if not self.is_valid_frame(frame_number):
            self._logger.warning(f"Frame {frame_number} out of range (0-{self._total_frames - 1})")
            return None
        if self._cap is None:
            return None
        self._cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = self._cap.read()
        if not ret:
            self._logger.warning(f"Failed to read frame {frame_number}")
            return None
        return frame

    def play_preview(self, start_frame: int, end_frame: int,
                     draw_extra: Callable[[np.ndarray, int], np.ndarray] = lambda f, i: f
                     ) -> tuple[Optional[np.ndarray], int]:
        last_frame = None
        pressed_key = -1
        while pressed_key == -1:
            for f in range(start_frame, end_frame + 1):
                frame = self.read_frame(f)
                if frame is None:
                    continue
                last_frame = frame
                frame = draw_extra(frame, f)
                cv2.imshow("AOI Coding Tool", frame)
                key = cv2.waitKey(int(1000 / PLAYBACK_FPS))
                if key != -1:
                    pressed_key = key
                    break
        final_frame = self.read_frame(end_frame)
        if final_frame is not None:
            final_frame = draw_extra(final_frame, end_frame)
            cv2.imshow("AOI Coding Tool", final_frame)
            last_frame = final_frame
        return last_frame, pressed_key

    def close(self) -> None:
        if self._cap is not None:
            self._cap.release()
            self._cap = None