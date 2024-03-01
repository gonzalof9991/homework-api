from datetime import datetime


def get_datetime_now() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def convert_str_to_datetime(date: str) -> datetime:
    return datetime.strptime(date, "%Y-%m-%d")


def convert_datetime_to_str(date: datetime) -> str:
    return date.strftime("%Y-%m-%d")


def compare_max_date(date: str) -> bool:
    start_date = convert_str_to_datetime(date)
    now = datetime.now()
    return start_date < now
