from django import forms
from django.core.validators import RegexValidator

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
        if start_date < datetime.date.today():
            raise ValidationError(_('Invalid date - new course starts in past'))
        return start_date

    def clean_end_date(self):
        start_date = self.cleaned_data['start_date']
        end_date = self.cleaned_data['end_date']
        if end_date < start_date:
            raise ValidationError(_('Invalid date - end date before start date'))
        return end_date

class StudentForm(forms.Form):
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
