"""
Custom domain exceptions for the Calendar Scheduler.
"""


class CalendarSchedulerError(Exception):
    """Base exception for all calendar scheduler errors."""


class CalendarDataError(CalendarSchedulerError):
    """Raised when calendar data cannot be loaded or is malformed."""


class InvalidMeetingError(CalendarSchedulerError):
    """Raised when a Meeting object contains invalid data."""


class SchedulingError(CalendarSchedulerError):
    """Raised when a scheduling operation fails."""
