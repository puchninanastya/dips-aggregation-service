from django import forms
from django.core.validators import RegexValidator, validate_comma_separated_integer_list
from datetime import datetime, date

class CourseForm(forms.Form):
    name = forms.CharField(
        max_length=60,
        widget=forms.TextInput(
            attrs={
            'placeholder':'Course name'
            }))
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
            'placeholder':'Course description'
            }))
    start_date = forms.DateField(
        widget=forms.TextInput(
            attrs={
            'placeholder':'Start date of this course'
            }))
    end_date = forms.DateField(
        widget=forms.TextInput(
            attrs={
            'placeholder':'End date of this course'
            }))
    price = forms.IntegerField(
        widget=forms.TextInput(
            attrs={
            'placeholder':'Course price'
            }))

    def clean_start_date(self):
        start_date = self.cleaned_data['start_date']
        if start_date < date.today():
            raise ValidationError(_('Invalid date - new course starts in past'))
        return start_date

    def clean_end_date(self):
        start_date = self.cleaned_data['start_date']
        end_date = self.cleaned_data['end_date']
        if end_date < start_date:
            raise ValidationError(_('Invalid date - end date before start date'))
        return end_date

class StudentForm(forms.Form):
    username = forms.CharField(
        max_length=60,
        widget=forms.TextInput(
            attrs={
            'placeholder':'Enter username'
            }))
    first_name = forms.CharField(
        max_length=60,
        widget=forms.TextInput(
            attrs={
            'placeholder':'Enter first name'
            }))
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
            'placeholder':'Enter last name'
            }))
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
            'placeholder':'Enter email address'
            }))
    phone_regex = RegexValidator(
        regex=r'^\++[7]+\d{10}$',
        message="Phone number must be entered in the format: '+79999999999'."
    )
    phone_number = forms.CharField(
        validators=[phone_regex],
        max_length=12,
        required=False,
        widget=forms.TextInput(
            attrs={
            'placeholder':'Enter phone number in format "+79999999999" '
            }))
    birth_date = forms.DateField(
        required=False,
        widget=forms.TextInput(
            attrs={
            'placeholder':'Enter birth date'
            }))
    height = forms.IntegerField(
        required=False,
        widget=forms.TextInput(
            attrs={
            'placeholder':'Enter height measurement'
            }))
    bust = forms.IntegerField(
        required=False,
        widget=forms.TextInput(
            attrs={
            'placeholder':'Enter bust measurement'
            }))
    waist = forms.IntegerField(
        required=False,
        widget=forms.TextInput(
            attrs={
            'placeholder':'Enter waist measurement'
            }))
    hips = forms.IntegerField(
        required=False,
        widget=forms.TextInput(
            attrs={
            'placeholder':'Enter hips measurement'
            }))
    shoe = forms.IntegerField(
        required=False,
        widget=forms.TextInput(
            attrs={
            'placeholder':'Enter shoe measurement'
            }))
    eyes = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
            'placeholder':'Enter eyes color'
            }),
        max_length=30)
    hair = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(
            attrs={
            'placeholder':'Enter hair color'
            }))

class OrderForm(forms.Form):
    user = forms.IntegerField(
        min_value=0,
        widget=forms.TextInput(
            attrs={
            'placeholder':'User id'
            }))
    order_date = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
            'placeholder':'Set datetime of order or null for autoset'
            }))
    courses = forms.CharField(
        validators=[validate_comma_separated_integer_list],
        widget=forms.TextInput(
            attrs={
            'placeholder':'Comma separated courses ids'
            }))

class PaymentForm(forms.Form):
    order_id = forms.IntegerField(
        min_value=0,
        widget=forms.TextInput(
            attrs={
            'placeholder':'Order id'
            }))
    payment_date = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(
            attrs={
            'placeholder':'Set date of payment or null for autoset'
            }))
    amount_paid = forms.IntegerField(
        widget=forms.TextInput(
            attrs={
            'placeholder':'Amount paid (in rubles)'
            }))
    PAYMENT_METHOD_CHOICES = (
        ('CH', "By cash"),
        ('CD', "By card")
    )
    payment_method = forms.ChoiceField(
        choices = PAYMENT_METHOD_CHOICES,
        required=True)
    account_number_regex = RegexValidator(
        regex=r'^\d{,20}$',
        message="This field should contain only digits."
    )
    account_number = forms.CharField(
        validators=[account_number_regex],
        max_length=20,
        required=False,
        widget=forms.TextInput(
            attrs={
            'placeholder':'Enter account number for payment by card" '
            }))
