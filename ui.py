from typing import Optional
import cv2
import numpy as np
from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT,
    COLOR_WHITE, COLOR_YELLOW, COLOR_GREEN, COLOR_RED, COLOR_GRAY, COLOR_BG,
    AOI_KEYS,
)


def _draw_text(frame: np.ndarray, text: str, x: int, y: int,
               color: tuple = COLOR_WHITE, scale: float = 0.5,
               thickness: int = 1) -> None:
    cv2.putText(frame, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX,
                scale, COLOR_BG, thickness + 2)
    cv2.putText(frame, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX,
                scale, color, thickness)


def draw_progress_bar(frame: np.ndarray, fraction: float,
                      x: int, y: int, width: int, height: int = 12) -> None:
    cv2.rectangle(frame, (x, y), (x + width, y + height), COLOR_GRAY, 1)
    fill_w = int(width * fraction)
    if fill_w > 0:
        cv2.rectangle(frame, (x, y), (x + fill_w, y + height), COLOR_GREEN, -1)


def draw_overlay(frame: np.ndarray,
                 fixation_idx: int, total: int,
                 start_frame: int, end_frame: int,
                 current_frame: int,
                 current_aoi: Optional[str],
                 previous_aoi: Optional[str],
                 video_time_sec: float,
                 progress_fraction: float) -> np.ndarray:
    overlay = frame.copy()
    h, w = overlay.shape[:2]

    help_y = h - 20
    help_text = "  ".join(f"{k}={v}" for k, v in AOI_KEYS.items())
    _draw_text(overlay, help_text, 10, h - 50, COLOR_YELLOW, 0.4)
    _draw_text(overlay, "Space=Prev  ←=PrevFix  →=Skip  R=Replay  Ctrl+S=Save  ESC=Exit  Z=Undo  P=Screen",
               10, h - 30, COLOR_GRAY, 0.4)

    _draw_text(overlay, f"Fixation: {fixation_idx + 1} / {total}", 10, 25, COLOR_YELLOW, 0.6)
    _draw_text(overlay, f"Frames: {start_frame} - {end_frame}", 10, 45)
    _draw_text(overlay, f"Current Frame: {current_frame}", 10, 65)

    aoi_display = current_aoi if current_aoi else "(empty)"
    _draw_text(overlay, f"Current AOI: {aoi_display}", 10, 85,
               COLOR_GREEN if current_aoi else COLOR_RED, 0.6)

    prev_display = previous_aoi if previous_aoi else "(none)"
    _draw_text(overlay, f"Previous AOI: {prev_display}", 10, 105)

    minutes = int(video_time_sec // 60)
    seconds = int(video_time_sec % 60)
    _draw_text(overlay, f"Video Time: {minutes}:{seconds:02d}", 10, 125)

    bar_x, bar_y = w // 2 - 150, h - 80
    _draw_text(overlay, f"{fixation_idx + 1} / {total}  {progress_fraction * 100:.1f}%",
               w // 2 - 40, bar_y - 10, COLOR_YELLOW, 0.5)
    draw_progress_bar(overlay, progress_fraction, bar_x, bar_y, 300, 14)

    return overlay


def resize_frame(frame: np.ndarray, width: int, height: int) -> np.ndarray:
    h, w = frame.shape[:2]
    scale = min(width / w, height / h)
    new_w, new_h = int(w * scale), int(h * scale)
    resized = cv2.resize(frame, (new_w, new_h))
    canvas = np.full((height, width, 3), COLOR_BG, dtype=np.uint8)
    y_off = (height - new_h) // 2
    x_off = (width - new_w) // 2
    canvas[y_off:y_off + new_h, x_off:x_off + new_w] = resized
    return canvas
