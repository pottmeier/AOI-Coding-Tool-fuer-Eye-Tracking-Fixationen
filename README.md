# AOI Coding Tool

Desktop-Anwendung zur manuellen AOI-Kodierung von Eye-Tracking-Fixationsdaten. Spielt jede Fixation als Videoloop ab — AOI-Zuweisung per Tastendruck.

## Voraussetzungen

- Python 3.11+
- pip

## Installation

```bash
# Repository klonen
git clone <repo-url> && cd AOI_Coding_Tool

# Venv anlegen und Abhängigkeiten installieren
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Nutzung

```bash
python main.py video.mp4 fixationen.csv
```

Oder ohne Argumente (dann Eingabe der Pfade im Terminal).

### CSV-Format

Die CSV muss folgende Spalten enthalten (Trennzeichen `;` oder `,` wird automatisch erkannt):

| Fixations_ID | Zeit | Start_Frame | End_Frame | Dauer (Frames) | AOI |
|---|---|---|---|---|---|

`AOI` darf leer sein — das Tool beginnt bei der ersten leeren Zeile.

### Shortcuts

| Taste | Aktion |
|---|---|
| `b` | BT |
| `g` | BG |
| `s` | SD |
| `1` | BL |
| `2` | BM |
| `3` | BR |
| `j` | BH |
| `h` | HS |
| `u` | U (Umgebung) |
| `Leertaste` | Vorheriges AOI wiederholen |
| `←` | Vorherige Fixation |
| `→` | Fixation überspringen |
| `R` | Loop wiederholen |
| `Z` | Letzte AOI rückgängig |
| `P` | Screenshot (PNG) |
| `Ctrl+S` | CSV speichern (speichert automatisch bei jeder Annotation) |
| `ESC` | Speichern & Beenden |

## Projektstruktur

```
config.py         – Konstanten, Key-Mapping, Farben
logger.py         – session.log
csv_manager.py    – CSV laden/speichern/verwalten
video_player.py   – OpenCV Frame-Lesen & Playback
ui.py             – Overlay, Progress-Bar, Resize
main.py           – Einstiegspunkt
requirements.txt  – Abhängigkeiten
```

## Logging

Das Tool erzeugt `session.log` mit allen Aktionen (Start, Annotationen, Fehler, Beenden).

## macOS-Hinweis

Falls `tkinter` nicht verfügbar ist (Python aus pyenv/homebrew): Das Tool verwendet nur OpenCV — die Dateiauswahl erfolgt über Kommandozeilen-Argumente oder Terminal-Eingabe.
