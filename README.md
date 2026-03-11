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
├── io_comp/                # Entry point package
│   ├── app.py              # CLI argument parsing and program entry point
│   └── __init__.py
├── models/                 # Domain model
│   ├── models.py           # Meeting class definition
│   └── __init__.py
├── services/               # Business logic
│   ├── calendar_service.py # Free-slot calculation algorithm
│   └── __init__.py
├── repositories/           # Data access layer
│   ├── csv_repository.py   # CSV parsing → Meeting objects
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
# Using defaults (Alice & Bob, 1-hour slot)
python -m io_comp.app

# Custom participants and duration
python -m io_comp.app --persons Alice Bob Carol --duration 90
```

Prints available time slots for the specified participants.

### Run Unit Tests

```bash
pytest
```

---

## Test Cases

- `test_no_slots_available` — A meeting blocks most of the day; no valid slot exists.
- `test_merged_overlap` — Two overlapping meetings from different people are merged into one block.
- `test_empty_calendar_full_day` — No meetings at all; the entire day is available.
- `test_basic_gap` — A clear gap between two meetings contains a valid slot.

---
