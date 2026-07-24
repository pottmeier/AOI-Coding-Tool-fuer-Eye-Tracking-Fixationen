from datetime import datetime
from config import LOG_FILE


class Logger:
    def __init__(self) -> None:
        self._file = LOG_FILE
        with open(self._file, "a") as f:
            f.write(f"\n--- Session started at {datetime.now():%Y-%m-%d %H:%M:%S} ---\n")

    def log(self, message: str) -> None:
        line = f"[{datetime.now():%H:%M:%S}] {message}\n"
        with open(self._file, "a") as f:
            f.write(line)

    def warning(self, message: str) -> None:
        line = f"[{datetime.now():%H:%M:%S}] WARNING: {message}\n"
        with open(self._file, "a") as f:
            f.write(line)

    def error(self, message: str) -> None:
        line = f"[{datetime.now():%H:%M:%S}] ERROR: {message}\n"
        with open(self._file, "a") as f:
            f.write(line)
