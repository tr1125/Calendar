"""
Domain models for the Calendar Scheduler.
"""
from dataclasses import dataclass
from datetime import time


@dataclass(frozen=True)
class Meeting:
    """
    Represents a scheduled meeting.
    Immutable by design (frozen=True) to prevent accidental mutation
    and shared-state bugs.
    """
    person_name: str
    name: str
    start_time: time
    end_time: time

    def __str__(self) -> str:
        return (
            f"Meeting(Person: {self.person_name}, Name: {self.name}, "
            f"Start Time: {self.start_time}, End Time: {self.end_time})"
        )
