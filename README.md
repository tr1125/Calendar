# Calendar Availability Finder

A scheduling tool that finds open time slots for meetings across multiple participants.

The system loads meeting data from a CSV file, processes it logically, and returns a list of time windows where all required participants are free — based on a requested meeting duration and defined working hours.

---

## Features

- **CSV Parsing** — Reads and processes raw data into structured `Meeting` objects.
- **Time Merge Algorithm** — Combines overlapping meetings from multiple participants into single blocked time ranges.
- **Available Slot Detection** — Calculates valid start/end windows based on the requested `Duration` and working hour boundaries (07:00–19:00).
- **Datetime Precision** — Resolves date synchronization issues by anchoring all `datetime` objects to a single consistent reference date.

---

## Project Structure

```
python-project/
├── io_comp/                # Main package
│   ├── app.py              # Core logic and program entry point
│   ├── Meeting.py          # Meeting class definition
│   └── __init__.py
├── resources/
│   └── calendar.csv        # Meeting data (name, title, start, end)
├── tests/
│   └── test_app.py         # Pytest unit tests
└── README.md
```

---

## Getting Started

### Prerequisites

- Python `3.12` or higher
- `pytest` for running tests

```bash
pip install pytest
```

### Run the Program

```bash
python -m io_comp.app
```

Prints available time slots for the default list of participants.

### Run Unit Tests

```bash
pytest
```

---

## Test Cases

- `test_no_slots_available` — A meeting blocks most of the day; no valid slot exists.
- `test_merged_overlap` — Two overlapping meetings from different people are merged into one block.
- `test_empty_calendar_full_day` — No meetings at all; the entire day is available.

---
