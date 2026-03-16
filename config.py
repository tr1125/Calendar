"""
Centralised configuration for the Calendar Scheduler.
All business-rule constants live here so they are easy to find and change.
"""
from datetime import time
from dataclasses import dataclass


@dataclass(frozen=True)
class SchedulerConfig:
    """Immutable configuration for the scheduler."""
    day_start: time = time(7, 0)
    day_end: time = time(19, 0)


# Default config used throughout the application
DEFAULT_CONFIG = SchedulerConfig()
