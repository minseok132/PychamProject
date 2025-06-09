# calendar_app/templatetags/duration_extras.py

from django import template

register = template.Library()

@register.filter
def format_duration(td):
    """
    - 1시간 이상 → HH:MMH
    - 1분 이상 → MM:SSH
    - 그 외      → 00:SSH
    """
    total = int(td.total_seconds())
    if total >= 3600:
        h = total // 3600
        m = (total % 3600) // 60
        return f"{h:02d}:{m:02d}H"
    if total >= 60:
        m = total // 60
        s = total % 60
        return f"{m:02d}:{s:02d}M"
    # 1분 미만
    s = total
    return f"00:{s:02d}S"
