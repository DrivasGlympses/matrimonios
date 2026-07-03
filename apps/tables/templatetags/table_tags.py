from django import template

register = template.Library()

@register.filter
def range_filter(value):
    """Returns a range from 0 to value-1"""
    try:
        return range(int(value))
    except (ValueError, TypeError):
        return range(0)

@register.filter
def range_from(start, end):
    """Returns a range from start to end-1"""
    try:
        return range(int(start), int(end))
    except (ValueError, TypeError):
        return range(0)
