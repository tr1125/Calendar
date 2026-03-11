"""
Unit tests for Calendar Scheduler Service
"""
import pytest
from datetime import time, timedelta
from services.calendar_service import find_available_slots
from models.models import Meeting

@pytest.fixture
def durations():
    """Fixture for common meeting durations"""
    return {
        "1h": timedelta(hours=1),
        "1.5h": timedelta(hours=1, minutes=30),
        "2h": timedelta(hours=2)
    }

def test_no_slots_available(durations):
    """Test case where no slots fit the requested duration"""
    # A long meeting that blocks almost the entire day
    mock_meetings = [
        Meeting("Bob", "Work", time(8, 0), time(18, 30))
    ]
    person_list = ["Bob"]
    
    # Requesting 2 hours, but only 1 hour is available in the morning (7-8)
    result = find_available_slots(person_list, durations["2h"], mock_meetings)
    
    assert len(result) == 0

def test_merged_overlap(durations):
    """Test that overlapping meetings from different people are merged correctly"""
    mock_meetings = [
        Meeting("Alice", "Alice Session", time(8, 0), time(9, 30)),
        Meeting("Bob", "Bob Session", time(9, 0), time(10, 0))
    ]
    person_list = ["Alice", "Bob"]
    
    result = find_available_slots(person_list, durations["1.5h"], mock_meetings)
    
    # Combined busy time is 08:00-10:00.
    # The first available 1.5h slot after that starts at 10:00 and ends at 17:30 
    # (since the day ends at 19:00).
    assert (time(10, 0), time(17, 30)) in result

def test_empty_calendar_full_day(durations):
    """Test that if the calendar is empty, the entire day is available"""
    mock_meetings = []
    person_list = ["Alice"]
    
    result = find_available_slots(person_list, durations["1h"], mock_meetings)
    
    # Expected window from 07:00 up to 18:00 (latest start for a 1h meeting)
    expected_window = (time(7, 0), time(18, 0))
    assert result[0] == expected_window

def test_basic_gap(durations):
    """Test finding a clear gap between two meetings"""
    mock_meetings = [
        Meeting("Alice", "Meeting A", time(8, 0), time(9, 0)),
        Meeting("Alice", "Meeting B", time(11, 0), time(12, 0))
    ]
    person_list = ["Alice"]
    
    result = find_available_slots(person_list, durations["1h"], mock_meetings)
    
    # Gap between 09:00 and 11:00 should allow a 1h meeting starting at 09:00 or 10:00
    assert (time(9, 0), time(10, 0)) in result