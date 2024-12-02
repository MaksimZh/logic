import datetime
import dateutil.parser


source = [
    "2024-05-13 14:30:00",
    "2024-05-13",
    "13.05.2024",
    "May 13 2024",
    "13 мая 2024",
    "20foo24-05-13",
]


def old(date_string: str):
    try:
        date = datetime.datetime.strptime(
            date_string, "%Y-%m-%d %H:%M:%S").date()
        print(f"Date: {date}")
    except ValueError as e:
        print(f"Error: {e}")

for s in source:
    old(s)


def new(date_string: str):
    try:
        date = dateutil.parser.parse(date_string).date()
        print(f"Date: {date}")
    except dateutil.parser.ParserError as e:
        print(f"Error: {e}")

for s in source:
    new(s)
