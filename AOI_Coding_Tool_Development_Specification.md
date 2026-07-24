# AOI Coding Tool -- Development Specification

## Goal

Develop a local Python desktop application for fast manual AOI
annotation of eye-tracking fixation data.

The application should minimize mouse usage by automatically navigating
to each fixation in the video and allowing AOIs to be assigned with a
single key press.

Target platform: **macOS**

---

# Technology Stack

- Python 3.11+
- OpenCV (`opencv-python`)
- pandas
- numpy
- openpyxl

GUI should use **OpenCV only** (`cv2.imshow()` and `cv2.waitKey()`).

Do not use Tkinter, Qt/PySide, Electron or web technologies.

---

# Input Files

## Video

- MP4
- 30 FPS
- User selects the file at startup.

## CSV

Required columns:

- Fixations_ID
- Zeit
- Start_Frame
- End_Frame
- Dauer (Frames)
- AOI

`AOI` may be empty.

---

# Startup

1.  Ask the user to select the video.
2.  Ask the user to select the CSV.
3.  Load the CSV.
4.  Find the first row where `AOI` is empty.
5.  If all rows are completed, display:

```{=html}
<!-- -->
```

    All fixations are already annotated.

and exit.

---

# Main Window

Single OpenCV window.

Window title:

    AOI Coding Tool

Preferred size:

    1600 x 900

Maintain aspect ratio when resizing.

---

# Playback Logic

For every fixation:

    Start_Frame
    End_Frame

calculate

    PreviewStart = max(0, End_Frame - 15)
    PreviewEnd = End_Frame + 15

Automatically play

    PreviewStart
    ...
    End_Frame
    ...
    PreviewEnd

at approximately **15 FPS**.

After playback, stop on **End_Frame**.

---

# Overlay

Display:

    Fixation: 384 / 2800

    Frames:
    18310 - 18342

    Current Frame:
    18342

    Current AOI:
    (empty)

    Previous AOI:
    BT

    Video Time:
    10:11

---

# Key Bindings

## AOIs

    b = BT
    g = BG
    s = SD
    1 = BL
    2 = BM
    3 = BR
    j = BH
    v = U

### Important

Current key mapping contains conflicts.

- `h` was previously assigned twice (`HS` and `BH`).
- `s` is assigned to `SD`, therefore saving should use `Ctrl+S`.

If `HS` is still required, assign another key (e.g. `j`).

---

# Navigation

Space

- Use previous AOI

Left Arrow

- Previous fixation

Right Arrow

- Skip fixation

r

- Replay preview

Ctrl+S

- Save CSV

ESC

- Save and exit

---

# AOI Assignment

When an AOI key is pressed:

1.  Write AOI into current CSV row.
2.  Immediately load the next empty fixation.

---

# Autosave

Automatically save every **20 annotations**.

---

# Resume

On startup always continue at the first row where AOI is empty.

---

# Performance

Never preload the entire video.

Read only required frames using

    cv2.VideoCapture.set(...)

---

# CSV Handling

Keep CSV in memory.

Write to disk only when

- Ctrl+S
- Autosave
- ESC

---

# Help Overlay

Display at the bottom:

    b  BT
    g  BG
    s  SD
    1  BL
    2  BM
    3  BR
    h  BH
    v  U

    Space = Previous AOI
    ← Previous
    → Skip
    R Replay
    Ctrl+S Save
    ESC Exit

---

# Progress Indicator

Display

    ████████████░░░░░░

    384 / 2800

    13.7 %

---

# Error Handling

If a fixation references a frame beyond the end of the video:

- Skip fixation
- Write warning to log

---

# Logging

Create

    session.log

Log

- Startup
- Autosaves
- Resume
- Manual saves
- Exit
- Errors

---

# Nice-to-have Features

## Zoom

Mouse wheel

- 1×
- 2×
- 4×

## Pan

Click + drag while zoomed.

## Undo

    z

Remove last AOI.

## Screenshot

    p

Save current frame as PNG.

---

# Architecture

Use an object-oriented design.

Suggested modules:

- `main.py`
- `config.py`
- `video_player.py`
- `csv_manager.py`
- `ui.py`
- `logger.py`

Requirements:

- Type hints
- Clear comments
- No unnecessary global variables
- Configuration centralized in `config.py`
- Separate responsibilities for video playback, CSV handling and UI
