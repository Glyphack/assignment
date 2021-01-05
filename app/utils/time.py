from datetime import datetime


def get_hour_quarter():
    time = datetime.now()
    if 0 <= time.minute < 15:
        return 1
    if 15 <= time.minute < 30:
        return 2
    if 30 <= time.minute < 45:
        return 3
    if 45 <= time.minute < 60:
        return 4
