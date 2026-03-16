"""
Calendar scheduling service.
Core business logic for finding free time slots across multiple participants.
"""
import logging
from datetime import datetime, timedelta, time, date
from typing import List, Tuple

from models.models import Meeting
from repositories.meeting_repository import MeetingRepository
from config import SchedulerConfig, DEFAULT_CONFIG
from exceptions import SchedulingError

logger = logging.getLogger(__name__)

# Type alias for a time window
TimeWindow = Tuple[time, time]


class CalendarService:
    """
    Service for finding available meeting slots.
    Repository and config are injected via the constructor (Dependency Injection).
    """

    def __init__(
        self,
        repository: MeetingRepository,
        config: SchedulerConfig = DEFAULT_CONFIG,
    ) -> None:
        self._repository = repository
        self._config = config

    def find_available_slots(
        self,
        person_list: List[str],
        event_duration: timedelta,
    ) -> List[TimeWindow]:
        """
        Find all free time windows in which all participants are available.

        Args:
            person_list:    Names of the required participants.
            event_duration: Required length of the meeting.

        Returns:
            List of (earliest_start, latest_start) time windows.

        Raises:
            SchedulingError: If event_duration exceeds the working day.
        """
        ref_date = datetime.today().date()
        day_start = datetime.combine(ref_date, self._config.day_start)
        day_end = datetime.combine(ref_date, self._config.day_end)

        if event_duration > day_end - day_start:
            raise SchedulingError(
                f"Requested duration {event_duration} exceeds the working day."
            )

        all_meetings = self._repository.load_meetings()
        busy_blocks = _collect_busy_blocks(person_list, all_meetings, ref_date)

        if not busy_blocks:
            logger.debug("No meetings found for %s — returning full day", person_list)
            return _full_day_window(day_start, day_end, event_duration)

        merged = _merge_overlapping(busy_blocks)
        return _gaps_as_windows(merged, day_start, day_end, event_duration)


# ---------------------------------------------------------------------------
# Private module-level helpers
# ---------------------------------------------------------------------------

def _collect_busy_blocks(
    person_list: List[str],
    all_meetings: List[Meeting],
    ref_date: date,
) -> List[Tuple[datetime, datetime]]:
    """Return sorted (start, end) datetime pairs for the relevant participants."""
    blocks = [
        (datetime.combine(ref_date, m.start_time), datetime.combine(ref_date, m.end_time))
        for m in all_meetings
        if m.person_name in person_list
    ]
    return sorted(blocks)


def _merge_overlapping(
    blocks: List[Tuple[datetime, datetime]],
) -> List[Tuple[datetime, datetime]]:
    """Merge overlapping/adjacent busy blocks into a minimal list."""
    merged: List[Tuple[datetime, datetime]] = []
    curr_start, curr_end = blocks[0]

    for next_start, next_end in blocks[1:]:
        if next_start <= curr_end:
            curr_end = max(curr_end, next_end)
        else:
            merged.append((curr_start, curr_end))
            curr_start, curr_end = next_start, next_end

    merged.append((curr_start, curr_end))
    return merged


def _full_day_window(
    day_start: datetime,
    day_end: datetime,
    event_duration: timedelta,
) -> List[TimeWindow]:
    """Return a single window covering the whole working day."""
    latest_start = day_end - event_duration
    return [(day_start.time(), latest_start.time())]


def _gaps_as_windows(
    merged: List[Tuple[datetime, datetime]],
    day_start: datetime,
    day_end: datetime,
    event_duration: timedelta,
) -> List[TimeWindow]:
    """Convert merged busy blocks into a list of available time windows."""
    windows: List[TimeWindow] = []
    last_end = day_start

    for block_start, block_end in merged:
        window_start = max(last_end, day_start)
        if block_start - window_start >= event_duration:
            latest_start = block_start - event_duration
            windows.append((window_start.time(), latest_start.time()))
        last_end = max(last_end, block_end)

    if day_end - last_end >= event_duration:
        windows.append((last_end.time(), (day_end - event_duration).time()))

    return windows
