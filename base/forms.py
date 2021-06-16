from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from base.models import ExchangeRate


class Add_data(forms.ModelForm):
    class Meta:
        model = ExchangeRate
        fields = ['currency', 'value']

    def clean_currency(self):
        currency = self.cleaned_data['currency']
        if not currency.isalpha():
            raise ValidationError('error text')
        return currency


class Search_data(forms.Form):
    currency = forms.CharField(max_length=5, label="Валюта")
    time = forms.CharField(max_length=255, label="Время", required=False)


class Convert_data(forms.Form):
    currency = forms.CharField(max_length=5, label="Валюта 1")
    currency2 = forms.CharField(max_length=5, label="Валюта 2")
    time = forms.CharField(max_length=255, label="Время", required=False)
    money = forms.DecimalField(label="Сумма")


class UserLoginForm(AuthenticationForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = {'username', 'password1', 'password2'}
