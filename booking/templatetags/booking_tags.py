from django import template
import math

register = template.Library()

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

@register.filter
def age_format(value, arg = None):
    if not is_number(value):
        return value

    ret = u""

    years = math.floor(value / 31536000)
    remainder = value % 31536000

    if years > 0:
        ret += u"%d year%s" % (years, "" if years == 1 else "s")

        if arg != None:
            return ret

    months = math.floor(remainder / 2592000)
    remainder = remainder % 2592000

    if months > 0:
        if (ret != ""):
            ret += " "

        ret += u"%d month%s" % (months, "" if months == 1 else "s")

        if arg != None:
            return ret

    days = math.floor(remainder / 86400)
    remainder = remainder % 86400

    if arg != None and days == 0:
        days = 1

    if days > 0:
        if (ret != ""):
            ret += " "

        ret += u"%d day%s" % (days, "" if days == 1 else "s")

        if arg != None:
            return ret

    if arg != None:
        raise RuntimeError("Value is strange, we should never arrive here!")

    hours = math.floor(remainder / 3600)
    remainder = remainder % 3600

    if hours > 0:
        if (ret != ""):
            ret += " "

        ret += u"%d hour%s" % (hours, "" if hours == 1 else "s")

    minutes = math.floor(remainder / 60)

    if minutes > 0:
        if (ret != ""):
            ret += " "

        ret += u"%d minute%s" % (minutes, "" if minutes == 1 else "s")

    seconds = round(remainder % 60)

    if seconds > 0:
        if (ret != ""):
            ret += " "

        ret += u"%d second%s" % (seconds, "" if seconds == 1 else "s")

    if ret == "":
        ret = "a few moments"

    return ret
