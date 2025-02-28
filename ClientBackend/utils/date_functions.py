from django.utils import timezone
from datetime import datetime, timedelta, date


def get_date_range_one_week_eariler_from_today(date: datetime):
    target_date = date
    start_of_day = timezone.make_aware(datetime(target_date.year, target_date.month,
                                                target_date.day, 0, 0, 0, 0)) - timedelta(days=11)
    end_of_day = timezone.make_aware(datetime(target_date.year, target_date.month,
                                              target_date.day, 23, 59, 59, 999999))
    return start_of_day.isoformat(), end_of_day.isoformat()


def convert_iso_to_datetime(date_string):
    dt = datetime.fromisoformat(date_string)
    if dt.tzinfo is None:
        dt = timezone.make_aware(dt)
    return dt


def convert_iso_to_date(date_string):
    return convert_iso_to_datetime(date_string).date()
