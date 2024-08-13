
from django import template

register = template.Library()

@register.filter
def range_filter(value):
    return range(value)

@register.filter
def subtract(value, arg):
    return value - arg

@register.simple_tag
def calculate_empty_stars(total, rating):
    return total - rating