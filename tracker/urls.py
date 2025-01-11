from django.urls import path
from . import views

urlpatterns = [
    path('', views.expense_list, name='expense_list'),
    path('add/', views.add_expense, name='add_expense'),
    path('edit/<int:expense_id>/', views.edit_expense, name='edit_expense'),
    path('delete/<int:expense_id>/', views.delete_expense, name='delete_expense'),
    path('login/', views.login, name='login'),
    path('reports/monthly/', views.monthly_report, name='monthly_report'),
    path('reports/export/csv/', views.export_csv, name='export_csv'),
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/mark/<int:notification_id>/', views.mark_notification_as_read, name='mark_notification_as_read'),
    path('test-email/', views.send_test_email, name='send_email'),
]