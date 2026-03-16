"""
Calendar Scheduler — application entry point.
"""
import argparse
import logging
from datetime import timedelta
from pathlib import Path

from repositories.csv_repository import CsvMeetingRepository
from services.calendar_service import CalendarService
from exceptions import CalendarSchedulerError

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Find available meeting slots for a group of people."
    )
    parser.add_argument(
        "--persons", nargs="+", default=["Alice", "Bob"],
        help="List of participant names (e.g. --persons Alice Bob Carol)",
    )
    parser.add_argument(
        "--duration", type=int, default=60,
        help="Required meeting duration in minutes (default: 60)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    project_root = Path(__file__).resolve().parent.parent
    csv_path = project_root / "resources" / "calendar.csv"

    # Dependency injection: construct repository and inject into service
    repository = CsvMeetingRepository(csv_path)
    service = CalendarService(repository)
    duration = timedelta(minutes=args.duration)

    try:
        available_slots = service.find_available_slots(args.persons, duration)

        logger.info("Found %d available slot(s):", len(available_slots))
        for start, end in available_slots:
            logger.info("  %s - %s", start.strftime("%H:%M"), end.strftime("%H:%M"))

    except CalendarSchedulerError as exc:
        logger.error("Scheduling failed: %s", exc)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
