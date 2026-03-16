"""
Abstract repository interface for meeting data.
Any concrete implementation (CSV, database, in-memory, etc.) must implement this.
"""
from abc import ABC, abstractmethod
from typing import List

from models.models import Meeting


class MeetingRepository(ABC):
    """Abstract base class defining the contract for meeting data access."""

    @abstractmethod
    def load_meetings(self) -> List[Meeting]:
        """Load and return all meetings."""
        ...
