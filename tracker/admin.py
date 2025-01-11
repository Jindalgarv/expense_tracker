from django.contrib import admin
from .models import *

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('title', 'amount', 'date', 'category', 'user')

admin.site.register(Category)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Notification)
# admin.site.register()

# Register your models here.
