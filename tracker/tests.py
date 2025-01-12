from django.test import TestCase
from .models import Expense, Category
from django.contrib.auth.models import User

class ExpenseTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password ="testpassword")
        self.category = Category.objects.create(name='Food')
        self.expense = Expense.objects.create(title='Pizza', amount=200, date='2021-07-01', category=self.category, user=self.user)
            
    def test_expense_list(self):
        response = self.client.get('/expense-list/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracker/expense_list.html')
        self.assertContains(response, 'Pizza')
        self.assertContains(response, '200')
        self.assertContains(response, '2021-07-01')

