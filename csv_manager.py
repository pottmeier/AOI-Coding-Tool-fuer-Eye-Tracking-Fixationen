from typing import Optional, Dict, Any
import pandas as pd
from config import AUTOSAVE_INTERVAL
from logger import Logger


class CsvManager:
    def __init__(self, logger: Logger) -> None:
        self._df: Optional[pd.DataFrame] = None
        self._path: Optional[str] = None
        self._current_index: int = 0
        self._annotations_since_save: int = 0
        self._logger = logger

    def load(self, path: str) -> None:
        self._df = pd.read_csv(path, sep=None, engine="python")
        self._path = path
        self._annotations_since_save = 0
        self._current_index = 0
        self._logger.log(f"Loaded CSV: {path} ({len(self._df)} rows)")

    @property
    def current_index(self) -> int:
        return self._current_index

    @current_index.setter
    def current_index(self, value: int) -> None:
        self._current_index = value

    @property
    def total(self) -> int:
        return len(self._df) if self._df is not None else 0

    @property
    def completed(self) -> bool:
        return self.next_empty() is None

    @property
    def annotation_count(self) -> int:
        return self._annotations_since_save

    def next_empty(self) -> Optional[int]:
        if self._df is None:
            return None
        empty_rows = self._df.index[self._df["AOI"].isna() | (self._df["AOI"] == "")].tolist()
        if not empty_rows:
            return None
        first_empty = empty_rows[0]
        self._current_index = first_empty
        return first_empty

    def row(self, row_idx: int) -> Dict[str, Any]:
        if self._df is None:
            return {}
        return self._df.iloc[row_idx].to_dict()

    def assign_aoi(self, row_idx: int, aoi: str) -> None:
        if self._df is None:
            return
        self._df.at[row_idx, "AOI"] = aoi
        self._annotations_since_save += 1

    def save(self) -> None:
        if self._df is None or self._path is None:
            return
        self._df.to_csv(self._path, index=False)
        self._annotations_since_save = 0
        self._logger.log(f"Saved CSV: {self._path}")

    def autosave(self) -> None:
        if self._df is None or self._path is None:
            return
        if self._annotations_since_save >= AUTOSAVE_INTERVAL:
            self.save()
            self._logger.log(f"Autosave at {self._current_index + 1}/{self.total}")

    def close(self) -> None:
        self.save()
