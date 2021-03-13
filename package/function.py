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
        'southafrica': 'SAST',
        'south_korea': 'GMT+9',
        'sydney': 'Australia/Sydney',
        'us_central': 'UTC-6',
        'us_east': 'EST',
        'us_south': 'EST',
        'us_west': 'PT',
        'vip_amsterdam': 'Europe/Amsterdam',
        'vip_us_east': 'EST',
        'vip_us_west': 'PT'
    }.get(var, 'UTC')
