from django.test import TestCase
from .models import Expense, Category
from django.contrib.auth.models import User
from datetime import datetime
from django.urls import reverse



class ExpenseTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password ="testpassword")
        self.client.login(username='testuser', password='testpassword')
        self.category = Category.objects.create(name='Food')
        self.expense = Expense.objects.create(title='Pizza', amount=200, date='2021-07-01', category=self.category, user=self.user)
            
    def test_expense_list(self):
        response = self.client.get(reverse('expense_list'))
        self.assertEqual(response.status_code, 200)
        formatted_date = datetime(2021, 7, 1).strftime('%B %-d, %Y')
        self.assertContains(response, formatted_date)



