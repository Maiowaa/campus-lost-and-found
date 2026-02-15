from django import template
from django.utils.dateformat import format as date_format

register = template.Library()


@register.filter
def format_date(value):
    """Format a date as 'Feb 15, 2026'."""
    if value:
        return date_format(value, 'M d, Y')
    return ''


@register.filter
def format_datetime(value):
    """Format a datetime as 'Feb 15, 2026 14:30'."""
    if value:
        return date_format(value, 'M d, Y H:i')
    return ''
