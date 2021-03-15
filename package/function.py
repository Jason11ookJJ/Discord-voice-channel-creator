from datetime import datetime
from pytz import timezone


def current_time():
    """
    return server time
    """
    return datetime.now().strftime("%d-%m-%y %H:%M:%S")


def time_zone_time(ctx):
    """
    return discord server time
    """
    return datetime.now(timezone(time_zone(ctx.guild.region.name))).strftime("%d-%m-%y %H:%M:%S")


def time_zone(var):
    """
    return discord server time zone
    """
    return {
        'amsterdam': 'Europe/Amsterdam',
        'brazil': '	America/Rio_Branco',
        'dubai': 'Asia/Dubai',
        'eu_central': 'CET',
        'eu_west': 'UTC',
        'europe': 'CET',
        'frankfurt': 'Europe/Berlin',
        'hongkong': 'Asia/Hong_Kong',
        'india': 'Africa/Nairobi',
        'japan': 'Asia/Tokyo',
        'london': 'Europe/London',
        'russia': 'Europe/Moscow',
        'singapore': 'Asia/Singapore',
        'southafrica': 'Africa/Johannesburg',
        'south_korea': 'Asia/Seoul',
        'sydney': 'Australia/Sydney',
        'us_central': 'US/Central',
        'us_east': 'US/East-Indiana',
        'us_south': 'US/Mountain',
        'us_west': 'US/Pacific',
        'vip_amsterdam': 'Europe/Amsterdam',
        'vip_us_east': 'US/East-Indiana',
        'vip_us_west': 'US/Pacific'
    }.get(var, 'UTC')
