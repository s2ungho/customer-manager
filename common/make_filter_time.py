from common.conv_time import conv_datetime


def make_filter_time(argument):
    time_key = argument['datetime_field']
    find_key = {}
    if 'from_datetime' in argument and len(argument['from_datetime']) > 0:
        from_datetime = conv_datetime(argument['from_datetime'])
        find_key[time_key] = {'$gte': from_datetime}

    if 'to_datetime' in argument and len(argument['to_datetime']) > 0:
        to_datetime = conv_datetime(argument['to_datetime'])
        if time_key in find_key:
            find_key[time_key]['$lte'] = to_datetime
        else:
            find_key[time_key] = {'$lte': to_datetime}
    return find_key
