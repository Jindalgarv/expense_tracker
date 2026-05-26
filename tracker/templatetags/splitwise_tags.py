from django import template
from django.utils import timezone

register = template.Library()


@register.filter
def abs_value(value):
    """Return the absolute value of a number."""
    try:
        return abs(value)
    except (TypeError, ValueError):
        return value


@register.filter
def currency(value):
    """Format a number as Indian Rupees currency string."""
    try:
        return '₹{:,.2f}'.format(float(value))
    except (TypeError, ValueError):
        return '₹0.00'


@register.filter
def initials(user):
    """Return the user's initials (first letter of first + last name)."""
    try:
        if user.first_name and user.last_name:
            return f"{user.first_name[0]}{user.last_name[0]}".upper()
        return user.username[:2].upper()
    except (AttributeError, IndexError):
        return '??'


@register.filter
def balance_class(value):
    """Return a CSS class name based on whether the value is positive, negative, or zero."""
    try:
        value = float(value)
        if value > 0:
            return 'positive'
        elif value < 0:
            return 'negative'
        return 'zero'
    except (TypeError, ValueError):
        return 'zero'


@register.filter
def avatar_color(user):
    """Return the user's avatar colour from their profile, with a safe fallback."""
    try:
        return user.profile.avatar_color
    except (AttributeError, Exception):
        return '#1dd1a1'


@register.filter
def time_since_short(value):
    """Return a short human-readable 'time ago' string.

    Examples: '2m', '1h', '3d', '2w', or a date string for older entries.
    """
    if value is None:
        return ''

    try:
        now = timezone.now()

        # Make value timezone-aware if it isn't already
        if timezone.is_naive(value):
            value = timezone.make_aware(value)

        diff = now - value
        total_seconds = int(diff.total_seconds())

        if total_seconds < 0:
            return 'just now'

        if total_seconds < 60:
            return f'{total_seconds}s'

        minutes = total_seconds // 60
        if minutes < 60:
            return f'{minutes}m'

        hours = minutes // 60
        if hours < 24:
            return f'{hours}h'

        days = hours // 24
        if days < 7:
            return f'{days}d'

        weeks = days // 7
        if weeks < 5:
            return f'{weeks}w'

        return value.strftime('%b %d')

    except (AttributeError, TypeError, ValueError):
        return ''
