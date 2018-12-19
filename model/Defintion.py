BAR_DICT = {
    'Date': 0,
    'Open': 1,
    'High': 2,
    'Low': 3,
    'Close': 4,
    'Volume': 5,
}


def dur_2_str(duration):
    if not isinstance(duration, list):
        duration_list = [duration]
    else:
        duration_list = duration

    duration_string_list = []
    for duration in duration_list:
        days = round(float(duration*(7/5)))
        if days >= 360:
            duration_string_list.append('{} Y'.format(round(days/365.0)))
        elif days > 30:
            duration_string_list.append('{} M'.format(round(days / 30.0)))
        else:
            duration_string_list.append('{} D'.format(round(days/10.0)*10))
    return duration_string_list




