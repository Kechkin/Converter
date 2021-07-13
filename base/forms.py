from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from base.models import ExchangeRate, ManagerSearchData


class AddData(forms.ModelForm):
    class Meta:
        model = ExchangeRate
        fields = ['currency', 'value']

    def clean_currency(self):
        currency = self.cleaned_data['currency']
        if not currency.isalpha():
            raise ValidationError('No digits in currency ')
        return currency


class SearchData(forms.Form):
    currency = forms.CharField(max_length=5, label="Валюта")
    time = forms.CharField(max_length=255, label="Время", required=False,
                           widget=forms.TextInput(attrs={'placeholder': '2021-05-27 12:22'}))

    def clean_currency(self):
        currency = self.cleaned_data['currency']
        if not currency.isalpha():
            raise ValidationError('No digits in currency ')
        return currency


class ConvertData(forms.Form):
    currency = forms.CharField(max_length=5, label="Валюта 1")
    currency2 = forms.CharField(max_length=5, label="Валюта 2")
    time = forms.CharField(max_length=255, label="Время", required=False,
                           widget=forms.TextInput(attrs={'placeholder': '2021-05-27 12:22'}))
    money = forms.DecimalField(label="Сумма")

    def clean_currency(self):
        currency = self.cleaned_data['currency']
        if not currency.isalpha():
            raise ValidationError('No digits in currency ')
        return currency

    def clean_currency2(self):
        currency2 = self.cleaned_data['currency2']
        if not currency2.isalpha():
            raise ValidationError('No digits in currency ')
        return currency2


class UserLoginForm(AuthenticationForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = {'username', 'password1', 'password2'}


class AverageValueForm(forms.Form):
    currency = forms.CharField(max_length=5, label="Валюта")
    currency2 = forms.CharField(max_length=5, label="Валюта")

    time = forms.CharField(max_length=255, label="Время", required=False,
                           widget=forms.TextInput(attrs={'placeholder': '2021-07-12 12:22'}))

    start = forms.CharField(max_length=255, label="Время", required=False,
                            widget=forms.TextInput(attrs={'placeholder': '2021-06-15 12:22'}))

    end = forms.CharField(max_length=255, label="Время", required=False,
                          widget=forms.TextInput(attrs={'placeholder': '2021-07-15 12:22'}))
