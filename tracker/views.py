from calendar import month
from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense, Category, Notification
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db.models import Q, Sum
from django.utils.timezone import now
import csv
from django.http import HttpResponse
from .utils import create_notification
from django.core.mail import send_mail
from django.http import HttpResponse

from io import StringIO
import csv
from django.http import HttpResponse
from .models import Expense
from django.contrib import messages



@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user)

    category_id = request.GET.get('category')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if category_id:
        expenses = expenses.filter(category_id=category_id)

    if start_date and end_date:
        expenses = expenses.filter(date__range=[start_date, end_date])

    categories = Category.objects.all()
    return render(request, 'tracker/expense_list.html', {'expenses': expenses,'categories': categories,'selected category': category_id, 'start_date': start_date, 'end_date': end_date})

@login_required
def add_expense(request):
    if request.method == 'POST':
        title = request.POST['title']
        amount = request.POST['amount']
        date = request.POST['date']
        category =  Category.objects.get(id=request.POST['category'])

        Expense.objects.create(
            title=title,
            amount=amount,
            date=date,
            category=category,
            user=request.user
        )
        create_notification(request.user, f'Bhai Naya kharaacha daala hai {title} pe {amount} rupaye ka')
        return redirect('expense_list')
    
    categories = Category.objects.all()
    return render(request, 'tracker/add_expense.html',{'categories': categories})

@login_required
def edit_expense(request, expense_id):
    expense= get_object_or_404(Expense, id=expense_id,user=request.user)
    if request.method == 'POST':
        expense.title = request.POST['title']
        expense.amount = request.POST['amount']
        expense.date = request.POST['date']
        expense.category = Category.objects.get(id=request.POST['category'])
        expense.save()
        return redirect('expense_list')
    categories = Category.objects.all()
    return render(request, 'tracker/edit_expense.html', {'expense': expense, 'categories': categories})

def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    if request.method == 'POST':
        expense.delete()
        return redirect('expense_list')
    return render(request, 'tracker/delete_expense.html', {'expense': expense})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('expense_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

MONTHS = {
    1: 'January', 2: 'February', 3: 'March', 4: 'April',
    5: 'May', 6: 'June', 7: 'July', 8: 'August',
    9: 'September', 10: 'October', 11: 'November', 12: 'December'
}

@login_required
def monthly_report(request):
    today = now()
    current_year = today.year

    # Fetch monthly expenses and annotate with totals
    monthly_expenses = Expense.objects.filter(
        user=request.user,
        date__year=current_year
    ).values('date__month').annotate(total=Sum('amount')).order_by('date__month')

    # Add the month name to each entry in the queryset
    for item in monthly_expenses:
        item['month'] = MONTHS[item['date__month']]  # Add month name to each item

    # Pass the updated data to the template
    return render(request, 'tracker/monthly_report.html', {
        'monthly_expenses': monthly_expenses,
        'current_year': current_year,
    })

@login_required
def export_csv(request, mail=False):
    # Create an in-memory buffer to store the CSV data
    csv_buffer = StringIO()
    writer = csv.writer(csv_buffer)

    # Write the header row
    writer.writerow(['Title', 'Amount', 'Date', 'Category', 'User'])

    # Fetch the user's expenses
    expenses = Expense.objects.filter(user=request.user).select_related('category')
    for expense in expenses:
        writer.writerow([
            expense.title,
            expense.amount,
            expense.date,
            expense.category.name,
            request.user.username
        ])

    # If the mail flag is True, return the CSV as a string
    if mail:
        return csv_buffer.getvalue()

    # Otherwise, return an HTTP response for downloading
    csv_buffer.seek(0)  # Reset the buffer pointer
    response = HttpResponse(csv_buffer, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=expenses.csv'
    return response

@login_required
def notifications(request):
    user_notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')
    print(user_notifications)
    print(request.user)
    return render(request, 'tracker/notification.html', {'notifications': user_notifications})

@login_required
def mark_notification_as_read(request, notification_id):
    notification = Notification.objects.get(id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('notifications')

from django.core.mail import EmailMessage

@login_required
def send_test_email(request):
    csv_data = export_csv(request, mail=True)

    email = EmailMessage(
        subject='Test Email from Jindal Expense Tracker',
        body='Dear User,\n\nHere is your CSV report. Please find it attached.\n\nBest regards,\nJindal Expense Tracker Team',
        from_email='garvjindal2@gmail.com',
        to=[f'{request.user.email}']
    )
    messages.success(request, 'Email Sent Successfully')
    

    email.attach('expenses.csv', csv_data, 'text/csv')

    email.send()

    return render(request, 'tracker/expense_list.html')

