# calendar_app/templatetags/format_extras.py

from django import template

register = template.Library()

@register.filter
def format_hours(value):
    """
    Decimal hour 값 → HH:MMH / MM:SSH / 00:SSS 포맷으로.
    """
    try:
        total_seconds = int(float(value) * 3600)
    except (TypeError, ValueError):
        return ""
    h = total_seconds // 3600
    m = (total_seconds % 3600) // 60
    s = total_seconds % 60

    if h:
        return f"{h:02d}:{m:02d}H"
    if m:
        return f"{m:02d}:{s:02d}M"
    return f"00:{s:02d}S"
