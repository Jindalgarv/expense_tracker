from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid


class UserProfile(models.Model):
    """Extended user profile with additional info."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, default='')
    currency = models.CharField(max_length=3, default='INR')
    avatar_color = models.CharField(max_length=7, default='#1dd1a1')

    def __str__(self):
        return f"{self.user.username}'s profile"

    def get_initials(self):
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name[0]}{self.user.last_name[0]}".upper()
        return self.user.username[:2].upper()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Auto-create a UserProfile when a new User is created."""
    if created:
        import random
        colors = ['#1dd1a1', '#5f27cd', '#ee5a24', '#0abde3', '#feca57', '#ff6b6b', '#54a0ff', '#00d2d3']
        UserProfile.objects.create(user=instance, avatar_color=random.choice(colors))


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save profile when user is saved."""
    if hasattr(instance, 'profile'):
        instance.profile.save()


class Category(models.Model):
    """Expense category with icon and color."""
    name = models.CharField(max_length=50)
    icon = models.CharField(max_length=10, default='📦')
    color = models.CharField(max_length=7, default='#6c757d')

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return f"{self.icon} {self.name}"


class Friendship(models.Model):
    """Friend connection between two users."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships_sent')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships_received')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f"{self.from_user.username} → {self.to_user.username} ({self.status})"


class Group(models.Model):
    """Expense sharing group."""
    GROUP_TYPES = [
        ('trip', '✈️ Trip'),
        ('home', '🏠 Home'),
        ('couple', '❤️ Couple'),
        ('friends', '👥 Friends'),
        ('work', '💼 Work'),
        ('other', '📋 Other'),
    ]
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default='')
    group_type = models.CharField(max_length=10, choices=GROUP_TYPES, default='friends')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_groups')
    simplify_debts = models.BooleanField(default=True)
    invite_code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_type_display_icon(self):
        icons = dict(self.GROUP_TYPES)
        display = icons.get(self.group_type, '📋')
        return display.split(' ')[0]


class GroupMembership(models.Model):
    """Link between a user and a group."""
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('member', 'Member'),
    ]
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='memberships')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_memberships')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('group', 'user')

    def __str__(self):
        return f"{self.user.username} in {self.group.name}"


class Expense(models.Model):
    """A shared expense that can be split among users."""
    SPLIT_CHOICES = [
        ('equal', 'Split Equally'),
        ('exact', 'Split by Exact Amounts'),
        ('percentage', 'Split by Percentage'),
        ('shares', 'Split by Shares'),
    ]
    description = models.CharField(max_length=200, blank=True, default='Expense')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    paid_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses_paid')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True, related_name='expenses')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    split_type = models.CharField(max_length=12, choices=SPLIT_CHOICES, default='equal')
    notes = models.TextField(blank=True, default='')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.description} — ₹{self.amount}"


class ExpenseSplit(models.Model):
    """Individual user's share of an expense."""
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='splits')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expense_splits')
    amount_owed = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        unique_together = ('expense', 'user')

    def __str__(self):
        return f"{self.user.username} owes ₹{self.amount_owed} for {self.expense.description}"


class Settlement(models.Model):
    """A payment from one user to another to settle debts."""
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='settlements_made')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='settlements_received')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, related_name='settlements')
    notes = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.from_user.username} paid ₹{self.amount} to {self.to_user.username}"


class Activity(models.Model):
    """Activity feed entry."""
    ACTION_TYPES = [
        ('expense_added', 'Expense Added'),
        ('expense_edited', 'Expense Edited'),
        ('expense_deleted', 'Expense Deleted'),
        ('settlement', 'Settlement Made'),
        ('group_created', 'Group Created'),
        ('member_added', 'Member Added'),
        ('member_removed', 'Member Removed'),
        ('friend_added', 'Friend Added'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    action_type = models.CharField(max_length=20, choices=ACTION_TYPES)
    description = models.TextField()
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)
    expense = models.ForeignKey(Expense, on_delete=models.SET_NULL, null=True, blank=True)
    settlement = models.ForeignKey(Settlement, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Activities'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.description}"


class Notification(models.Model):
    """User notification."""
    NOTIFICATION_TYPES = [
        ('expense', 'Expense'),
        ('settlement', 'Settlement'),
        ('friend_request', 'Friend Request'),
        ('group', 'Group'),
        ('reminder', 'Reminder'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='expense')
    is_read = models.BooleanField(default=False)
    link = models.CharField(max_length=200, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:50]}"


class PushSubscription(models.Model):
    """Stores Web Push API subscription data for a user's device."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='push_subscriptions')
    endpoint = models.URLField(max_length=500)
    p256dh = models.CharField(max_length=200)
    auth = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'endpoint')

    def __str__(self):
        return f"Push Subscription for {self.user.username}"
