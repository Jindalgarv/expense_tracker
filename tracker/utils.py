from decimal import Decimal, ROUND_HALF_UP

from .services import create_notification as _create_notification


def create_notification(user, message, notification_type='expense', link=''):
    """
    Create a notification for *user*.

    Delegates to ``services.create_notification``.
    """
    return _create_notification(
        user=user,
        message=message,
        notification_type=notification_type,
        link=link,
    )


def format_currency(amount):
    """
    Format a ``Decimal`` (or numeric) *amount* as an INR string.

    Example::

        >>> format_currency(Decimal('1234.5'))
        '₹1,234.50'
    """
    amount = Decimal(str(amount)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    sign = ''
    if amount < 0:
        sign = '-'
        amount = abs(amount)

    integer_part, decimal_part = str(amount).split('.')

    # Indian numbering: first group of 3, then groups of 2.
    if len(integer_part) <= 3:
        formatted_int = integer_part
    else:
        last_three = integer_part[-3:]
        remaining = integer_part[:-3]
        # Group the remaining digits in pairs from right to left.
        groups = []
        while remaining:
            groups.append(remaining[-2:])
            remaining = remaining[:-2]
        groups.reverse()
        formatted_int = ','.join(groups) + ',' + last_three

    return f'{sign}₹{formatted_int}.{decimal_part}'