from .models import Notification, Friendship
from django.db.models import Q


def global_context(request):
    """Add global context variables available in all templates."""
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(
            user=request.user, is_read=False
        ).count()
        pending_requests = Friendship.objects.filter(
            to_user=request.user, status='pending'
        ).count()
        return {
            'unread_notifications_count': unread_notifications,
            'pending_requests_count': pending_requests,
        }
    return {
        'unread_notifications_count': 0,
        'pending_requests_count': 0,
    }
