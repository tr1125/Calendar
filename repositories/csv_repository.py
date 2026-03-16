"""
CSV-backed implementation of MeetingRepository.
"""
import csv
import logging
from datetime import datetime
from pathlib import Path
from typing import List

from models.models import Meeting
from repositories.meeting_repository import MeetingRepository
from exceptions import CalendarDataError, InvalidMeetingError

logger = logging.getLogger(__name__)


class CsvMeetingRepository(MeetingRepository):
    """Loads meetings from a CSV file."""

    def __init__(self, file_path: Path) -> None:
        self._file_path = file_path

    def load_meetings(self) -> List[Meeting]:
        """Load and return all meetings from the CSV file."""
        if not self._file_path.exists():
            raise CalendarDataError(f"CSV file not found at: {self._file_path}")

        meetings: List[Meeting] = []
        logger.info("Loading meetings from %s", self._file_path)

        try:
            with open(self._file_path, mode="r", encoding="utf-8") as file:
                reader = csv.reader(file)
                for line_num, row in enumerate(reader, start=1):
                    meeting = self._parse_row(row, line_num)
                    if meeting is not None:
                        meetings.append(meeting)
        except OSError as exc:
            raise CalendarDataError(f"Failed to read CSV file: {self._file_path}") from exc

        logger.info("Loaded %d meetings", len(meetings))
        return meetings

    def _parse_row(self, row: List[str], line_num: int) -> Meeting | None:
        """Parse a single CSV row into a Meeting. Returns None for blank/short rows."""
        if not row or len(row) < 4:
            return None
        try:
            start_time = datetime.strptime(row[2].strip(), "%H:%M").time()
            end_time = datetime.strptime(row[3].strip(), "%H:%M").time()
        except ValueError as exc:
            raise InvalidMeetingError(
                f"Invalid time format on line {line_num}: {row}"
            ) from exc

        return Meeting(
            person_name=row[0].strip(),
            name=row[1].strip(),
            start_time=start_time,
            end_time=end_time,
        )
