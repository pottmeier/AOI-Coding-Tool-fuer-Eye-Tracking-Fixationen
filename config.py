from typing import Dict, Optional

# Window
WINDOW_TITLE: str = "AOI Coding Tool"
WINDOW_WIDTH: int = 1600
WINDOW_HEIGHT: int = 900

# Video
VIDEO_FPS: int = 30
PLAYBACK_FPS: int = 15
PREVIEW_BEFORE: int = 15
PREVIEW_AFTER: int = 15

# CSV
CSV_DELIMITER: str = ","
AUTOSAVE_INTERVAL: int = 20

# Colors (BGR)
COLOR_WHITE: tuple = (255, 255, 255)
COLOR_YELLOW: tuple = (0, 255, 255)
COLOR_GREEN: tuple = (0, 255, 0)
COLOR_RED: tuple = (0, 0, 255)
COLOR_GRAY: tuple = (128, 128, 128)
COLOR_BG: tuple = (40, 40, 40)

# AOI key mapping
AOI_KEYS: Dict[str, str] = {
    "b": "BT",
    "g": "BG",
    "s": "SD",
    "1": "BL",
    "2": "BM",
    "3": "BR",
    "j": "BH",
    "h": "HS",
    "u": "U",
}

# Cross-platform key codes (raw values from cv2.waitKey())
# Each platform returns different raw values for the same physical key
# Linux GTK | Windows | macOS Cocoa
KEY_LEFT: set = {65361, 2424832, 63234}
KEY_RIGHT: set = {65363, 2555904, 63235}
KEY_ESC: int = 27

# Log file
LOG_FILE: str = "session.log"
