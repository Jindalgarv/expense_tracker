from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Group, Expense, Settlement, Category


class UserRegisterForm(UserCreationForm):
    """Registration form with extended user fields."""
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Choose a username',
        }),
    )
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'First name',
        }),
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Last name',
        }),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Email address',
        }),
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Create a password',
        }),
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Confirm your password',
        }),
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class UserProfileForm(forms.Form):
    """Form for editing user profile information."""
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'First name',
        }),
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Last name',
        }),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Email address',
        }),
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Phone number',
        }),
    )


class GroupForm(forms.ModelForm):
    """Form for creating and editing expense groups."""

    class Meta:
        model = Group
        fields = ['name', 'description', 'group_type', 'simplify_debts']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. Goa Trip 2026',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'What is this group for?',
                'rows': 3,
            }),
            'group_type': forms.Select(attrs={
                'class': 'form-input',
            }),
            'simplify_debts': forms.CheckboxInput(attrs={
                'class': 'form-input',
            }),
        }


class ExpenseForm(forms.ModelForm):
    """Form for creating and editing expenses."""

    class Meta:
        model = Expense
        fields = ['description', 'amount', 'date', 'category', 'split_type', 'notes']
        widgets = {
            'description': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'What was this expense for?',
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0.01',
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date',
            }),
            'category': forms.Select(attrs={
                'class': 'form-input',
            }),
            'split_type': forms.Select(attrs={
                'class': 'form-input',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Any additional notes…',
                'rows': 3,
            }),
        }


class SettlementForm(forms.Form):
    """Form for recording a settlement payment between friends."""
    to_user = forms.ModelChoiceField(
        queryset=User.objects.none(),
        label='Pay to',
        widget=forms.Select(attrs={
            'class': 'form-input',
        }),
    )
    amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-input',
            'placeholder': '0.00',
            'step': '0.01',
            'min': '0.01',
        }),
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-input',
            'type': 'date',
        }),
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-input',
            'placeholder': 'Optional notes…',
            'rows': 3,
        }),
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            from .models import Friendship
            from django.db.models import Q

            accepted = Friendship.objects.filter(
                Q(from_user=user, status='accepted') | Q(to_user=user, status='accepted')
            )
            friend_ids = set()
            for friendship in accepted:
                if friendship.from_user_id == user.id:
                    friend_ids.add(friendship.to_user_id)
                else:
                    friend_ids.add(friendship.from_user_id)

            self.fields['to_user'].queryset = User.objects.filter(id__in=friend_ids)