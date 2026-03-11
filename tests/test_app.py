"""
Unit tests for Comp calendar scheduler
"""
import pytest
from datetime import time, timedelta
from io_comp.app import find_available_slots
from io_comp.Meeting import Meeting


def test_find_available_slots():
    """Test finding available time slots"""
    assert True



# פיקסצ'ר בסיסי להגדרת זמנים משותפים
@pytest.fixture
def durations():
    return {
        "1h": timedelta(hours=1),
        "1.5h": timedelta(hours=1, minutes=30)
    }

def test_no_slots_available():
    """Test case where no slots fit the duration"""
    from datetime import time, timedelta
    from io_comp.Meeting import Meeting

    # פגישה ארוכה מאוד שחוסמת את רוב היום
    mock_meetings = [Meeting("Bob","Work", time(8, 0), time(18, 30) )]
    person_list = ["Bob"]
    duration = timedelta(hours=2) # אין חלון של שעתיים רצופות
    
    result = find_available_slots(person_list, duration, mock_meetings)
    
    assert len(result) == 0

def test_merged_overlap(durations):
    """טסט 2: בדיקה שחפיפה בין שני אנשים מאוחדת לחסימה אחת"""
    mock_meetings = [
        Meeting("Alice", "Alice Session", time(8, 0), time(9, 30)),
        Meeting("Bob", "Bob Session", time(9, 0), time(10, 0))
    ]
    person_list = ["Alice", "Bob"]
    
    result = find_available_slots(person_list, durations["1.5h"], mock_meetings)
    
    # הזמן התפוס המאוחד הוא 08:00-10:00.
    # הפגישה הבאה יכולה להתחיל רק ב-10:00.
    assert (time(10, 0), time(17, 30)) in result

def test_empty_calendar_full_day(durations):
    """טסט 3: בדיקה שכאשר אין פגישות, כל היום פנוי"""
    mock_meetings = []
    person_list = ["Alice"]
    
    result = find_available_slots(person_list, durations["1h"], mock_meetings)
    
    # מצפים לחלון מ-07:00 עד 18:00
    assert result[0] == (time(7, 0), time(18, 0))