from datetime import datetime as dt


def time_ago(timestamp_tz):
    now = dt.utcnow().replace(tzinfo=timestamp_tz.tzinfo)
    diff = now - timestamp_tz

    if diff.days > 365:
        years = diff.days // 365
        return f"{years} year{'s' if years > 1 else ''} ago"
    if diff.days > 30:
        months = diff.days // 30
        return f"{months} month{'s' if months > 1 else ''} ago"
    if diff.days > 0:
        return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
    if diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    if diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    if diff.seconds > 0:
        return f"{diff.seconds} second{'s' if diff.seconds > 1 else ''} ago"
    return "just now"
