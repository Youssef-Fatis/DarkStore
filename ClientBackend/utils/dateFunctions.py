from datetime import datetime, timedelta


def get_date_from_one_week_earlier_to_date(date: datetime):
    target_date = date
    start_of_day = datetime(target_date.year, target_date.month,
                            target_date.day, 0, 0, 0, 0) - timedelta(days=8)
    end_of_day = datetime(target_date.year, target_date.month,
                          target_date.day, 23, 59, 59, 999000)
    return start_of_day, end_of_day


def format_to_iso(dates):
    start_iso = dates[0].isoformat()
    end_iso = dates[1].isoformat()
    return start_iso, end_iso
