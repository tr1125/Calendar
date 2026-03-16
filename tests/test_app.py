"""
Unit tests for Calendar Scheduler Service.
Uses an in-memory FakeMeetingRepository — no CSV files, no I/O.
"""
import pytest
from datetime import time, timedelta
from typing import Dict, List

from models.models import Meeting
from repositories.meeting_repository import MeetingRepository
from services.calendar_service import CalendarService
from config import SchedulerConfig
from exceptions import SchedulingError


# ---------------------------------------------------------------------------
# Fake repository (in-memory implementation of the abstract interface)
# ---------------------------------------------------------------------------

class FakeMeetingRepository(MeetingRepository):
    """Test double: returns a fixed list of meetings with no I/O."""

    def __init__(self, meetings: List[Meeting]) -> None:
        self._meetings = meetings

    def load_meetings(self) -> List[Meeting]:
        return list(self._meetings)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def durations() -> Dict[str, timedelta]:
    return {
        "1h":   timedelta(hours=1),
        "1.5h": timedelta(hours=1, minutes=30),
        "2h":   timedelta(hours=2),
    }


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_no_slots_available(durations: Dict[str, timedelta]) -> None:
    """No slot fits when a single long meeting blocks almost the entire day."""
    repo = FakeMeetingRepository([
        Meeting("Bob", "Work", time(8, 0), time(18, 30)),
    ])
    result = CalendarService(repo).find_available_slots(["Bob"], durations["2h"])
    assert len(result) == 0


def test_merged_overlap(durations: Dict[str, timedelta]) -> None:
    """Overlapping meetings from different people are merged before gap detection."""
    repo = FakeMeetingRepository([
        Meeting("Alice", "Alice Session", time(8, 0), time(9, 30)),
        Meeting("Bob",   "Bob Session",   time(9, 0), time(10, 0)),
    ])
    result = CalendarService(repo).find_available_slots(["Alice", "Bob"], durations["1.5h"])
    # Combined busy: 08:00–10:00 → first window starts at 10:00, latest start 17:30
    assert (time(10, 0), time(17, 30)) in result


def test_empty_calendar_full_day(durations: Dict[str, timedelta]) -> None:
    """An empty calendar returns a single window covering the whole working day."""
    repo = FakeMeetingRepository([])
    result = CalendarService(repo).find_available_slots(["Alice"], durations["1h"])
    assert result[0] == (time(7, 0), time(18, 0))


def test_basic_gap(durations: Dict[str, timedelta]) -> None:
    """A clear gap between two meetings is detected correctly."""
    repo = FakeMeetingRepository([
        Meeting("Alice", "Meeting A", time(8, 0),  time(9, 0)),
        Meeting("Alice", "Meeting B", time(11, 0), time(12, 0)),
    ])
    result = CalendarService(repo).find_available_slots(["Alice"], durations["1h"])
    assert (time(9, 0), time(10, 0)) in result


def test_custom_config(durations: Dict[str, timedelta]) -> None:
    """SchedulerConfig is respected — shorter day yields fewer slots."""
    short_day = SchedulerConfig(day_start=time(9, 0), day_end=time(11, 0))
    repo = FakeMeetingRepository([])
    result = CalendarService(repo, config=short_day).find_available_slots(["Alice"], durations["1h"])
    assert result == [(time(9, 0), time(10, 0))]


def test_duration_exceeds_day_raises(durations: Dict[str, timedelta]) -> None:
    """SchedulingError is raised when requested duration exceeds the working day."""
    repo = FakeMeetingRepository([])
    with pytest.raises(SchedulingError):
        CalendarService(repo).find_available_slots(["Alice"], timedelta(hours=13))


def test_irrelevant_persons_ignored(durations: Dict[str, timedelta]) -> None:
    """Meetings for people not in person_list are not counted as busy."""
    repo = FakeMeetingRepository([
        Meeting("Carol", "All day", time(7, 0), time(19, 0)),
    ])
    result = CalendarService(repo).find_available_slots(["Alice"], durations["1h"])
    # Carol's meeting should not block Alice
    assert len(result) > 0
