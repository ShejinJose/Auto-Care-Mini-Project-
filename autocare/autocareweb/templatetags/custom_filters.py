from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Template filter to get an item from a dictionary using its key
    Usage: {{ my_dict|get_item:key }}
    """
    return dictionary.get(key)


from django import template
from datetime import timedelta, datetime

register = template.Library()

@register.filter
def add_days(value, days):
    """Adds a specified number of days to a given date."""
    if isinstance(value, (str, int, float)):
        value = datetime.strptime(value, "%Y-%m-%d").date()
    return value + timedelta(days=days)
