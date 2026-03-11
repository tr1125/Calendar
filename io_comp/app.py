"""
This is the App entry point
"""
import argparse
from datetime import timedelta
from repositories.csv_repository import load_meetings
from services.calendar_service import find_available_slots
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="Find available meeting slots for a group of people.")
    parser.add_argument(
        "--persons", nargs="+", default=["Alice", "Bob"],
        help="List of participant names (e.g. --persons Alice Bob Carol)"
    )
    parser.add_argument(
        "--duration", type=int, default=60,
        help="Required meeting duration in minutes (default: 60)"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Setup paths
    project_root = Path(__file__).resolve().parent.parent
    csv_path = project_root / 'resources' / 'calendar.csv'
    try:
        # 1. Fetch data through DAL
        all_meetings = load_meetings(csv_path)

        # 2. Define business request
        person_list = args.persons
        duration = timedelta(minutes=args.duration)

        # 3. Execute logic through Service
        available_slots = find_available_slots(person_list, duration, all_meetings)

        # 4. Display results
        print(f"Found {len(available_slots)} available slots:")
        for start, end in available_slots:
            print(f"{start.strftime('%H:%M')} - {end.strftime('%H:%M')}")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
