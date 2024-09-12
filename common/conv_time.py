from datetime import datetime


def conv_datetime(datetime_string):
    if len(datetime_string) > 19:
        dt = datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S.%f")
    else:
        dt = datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S")
    return dt
