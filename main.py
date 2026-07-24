import sys
import os
import cv2
import numpy as np
import pandas as pd
from config import WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT, AOI_KEYS, KEY_LEFT, KEY_RIGHT
from logger import Logger
from csv_manager import CsvManager
from video_player import VideoPlayer
from ui import draw_overlay, resize_frame


def resolve_path(path: str) -> str:
    path = os.path.expanduser(path)
    if not os.path.isfile(path):
        sys.exit(f"File not found: {path}")
    return path


def main() -> None:
    logger = Logger()
    logger.log("Application started")

    if len(sys.argv) >= 3:
        video_path = resolve_path(sys.argv[1])
        csv_path = resolve_path(sys.argv[2])
    else:
        video_path = resolve_path(input("Video path: ").strip())
        csv_path = resolve_path(input("CSV path: ").strip())

    csv_mgr = CsvManager(logger)
    video = VideoPlayer(logger)

    csv_mgr.load(csv_path)
    video.open(video_path)

    first_empty = csv_mgr.next_empty()
    if first_empty is None:
        print("All fixations are already annotated.")
        logger.log("All fixations already annotated — exiting")
        video.close()
        return

    cv2.namedWindow(WINDOW_TITLE, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT)

    current_idx = first_empty
    previous_aoi = None
    annotation_history = []
    last_used_aoi = None

    while current_idx < csv_mgr.total:
        row_data = csv_mgr.row(current_idx)
        start_frame = int(row_data["Start_Frame"])
        end_frame = int(row_data["End_Frame"])
        current_aoi = row_data.get("AOI", "")
        if pd.isna(current_aoi):
            current_aoi = ""

        if not video.is_valid_frame(end_frame):
            logger.warning(f"Fixation {current_idx + 1}: End_Frame {end_frame} out of range, skipping")
            csv_mgr.assign_aoi(current_idx, "SKIP")
            csv_mgr.save()
            current_idx += 1
            continue

        def _draw(frame, cur_frame):
            p = current_idx / csv_mgr.total if csv_mgr.total > 0 else 0
            d = resize_frame(frame, WINDOW_WIDTH, WINDOW_HEIGHT)
            return draw_overlay(d, current_idx, csv_mgr.total, start_frame, end_frame, cur_frame,
                                current_aoi if current_aoi else None, previous_aoi,
                                cur_frame / 30.0, p)

        final_frame, key = video.play_preview(start_frame, end_frame, draw_extra=_draw)
        if final_frame is None:
            logger.error(f"Fixation {current_idx + 1}: could not read frames, skipping")
            current_idx += 1
            continue

        while True:
            video_time = end_frame / 30.0
            frame_display = _draw(final_frame, end_frame)
            cv2.imshow(WINDOW_TITLE, frame_display)

            if key == -1:
                key = cv2.waitKey(0)

            mk = key & 0xFF

            try:
                aoi_key = chr(mk)
            except ValueError:
                aoi_key = ""
            if aoi_key in AOI_KEYS:
                aoi = AOI_KEYS[aoi_key]
                old_value = csv_mgr.row(current_idx).get("AOI", "")
                if pd.isna(old_value):
                    old_value = ""
                annotation_history.append((current_idx, old_value))
                csv_mgr.assign_aoi(current_idx, aoi)
                csv_mgr.save()
                previous_aoi = aoi
                last_used_aoi = aoi
                logger.log(f"Fixation {current_idx + 1}: assigned AOI={aoi}")
                next_empty = csv_mgr.next_empty()
                if next_empty is None:
                    current_idx = csv_mgr.total
                else:
                    current_idx = next_empty
                break

            if mk == ord(" "):
                if last_used_aoi:
                    old_value = csv_mgr.row(current_idx).get("AOI", "")
                    if pd.isna(old_value):
                        old_value = ""
                    annotation_history.append((current_idx, old_value))
                    csv_mgr.assign_aoi(current_idx, last_used_aoi)
                    csv_mgr.save()
                    previous_aoi = last_used_aoi
                    logger.log(f"Fixation {current_idx + 1}: assigned AOI={last_used_aoi} (space)")
                    next_empty = csv_mgr.next_empty()
                    if next_empty is None:
                        current_idx = csv_mgr.total
                    else:
                        current_idx = next_empty
                    break

            if key in KEY_LEFT:
                if current_idx > 0:
                    current_idx -= 1
                    break

            if key in KEY_RIGHT:
                logger.log(f"Fixation {current_idx + 1}: skipped")
                current_idx += 1
                break

            if mk == ord("r") or mk == ord("R"):
                final_frame, key = video.play_preview(start_frame, end_frame, draw_extra=_draw)
                continue

            if mk == ord("z") or mk == ord("Z"):
                if annotation_history:
                    row_idx, old_val = annotation_history.pop()
                    csv_mgr._df.at[row_idx, "AOI"] = old_val
                    csv_mgr.save()
                    current_idx = row_idx
                    current_aoi = old_val
                    logger.log(f"Undo: fixation {row_idx + 1} reverted to '{old_val}'")
                    row_data = csv_mgr.row(current_idx)
                    start_frame = int(row_data["Start_Frame"])
                    end_frame = int(row_data["End_Frame"])
                    final_frame, key = video.play_preview(start_frame, end_frame, draw_extra=_draw)
                continue

            if mk == ord("p") or mk == ord("P"):
                cv2.imwrite(f"fixation_{current_idx + 1}_frame_{end_frame}.png", final_frame)
                logger.log(f"Screenshot: fixation_{current_idx + 1}_frame_{end_frame}.png")
                continue

            if mk == 19:
                csv_mgr.save()
                continue

            if key == 27:
                csv_mgr.close()
                video.close()
                cv2.destroyAllWindows()
                logger.log("Application exited (ESC)")
                return

            key = -1  # undefined key → wait for next

    csv_mgr.close()
    video.close()
    cv2.destroyAllWindows()
    logger.log("All fixations annotated — exiting")
    print("All fixations annotated!")


if __name__ == "__main__":
    main()
