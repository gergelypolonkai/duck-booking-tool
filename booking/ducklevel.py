from django.conf import settings
import math

def level_to_up_minutes(level):
    if level == 0:
        return 0

    return 2 * pow(10, level)

def level_to_down_minutes(level):
    if level == 0:
        return 0

    return 20 * pow(10, level)

def minutes_to_level(up_minutes, down_minutes):
    minutes = up_minutes + down_minutes / 10
    level = 0 if minutes <= 0 else min(settings.MAX_DUCK_LEVEL, math.floor(math.log10(minutes)))

    return level
