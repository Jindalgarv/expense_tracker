from django.contrib import admin
from .models import (
    UserProfile, Category, Friendship, Group, GroupMembership,
    Expense, ExpenseSplit, Settlement, Activity, Notification
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'currency', 'avatar_color')
    search_fields = ('user__username', 'user__email')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'color')


@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'status', 'created_at')
    list_filter = ('status',)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'group_type', 'created_by', 'simplify_debts', 'created_at')
    list_filter = ('group_type',)
    search_fields = ('name',)


@admin.register(GroupMembership)
class GroupMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'group', 'role', 'joined_at')
    list_filter = ('role',)


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('description', 'amount', 'date', 'paid_by', 'group', 'split_type', 'category')
    list_filter = ('split_type', 'category', 'group')
    search_fields = ('description',)
    date_hierarchy = 'date'


@admin.register(ExpenseSplit)
class ExpenseSplitAdmin(admin.ModelAdmin):
    list_display = ('expense', 'user', 'amount_owed')


@admin.register(Settlement)
class SettlementAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'amount', 'date', 'group')
    date_hierarchy = 'date'


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'action_type', 'description', 'created_at')
    list_filter = ('action_type',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read')
