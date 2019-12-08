from django.forms import ModelForm
from sign_in.models import LoginValue
from django import forms

"""

class RegisterForm(ModelForm):
    class Meta:
        model = LoginValue
        fields = ['login', 'phone_number', 'iin', 'name', 'surname', 'password', 'password1']
"""


class RegisterForm(forms.Form):
    login = forms.CharField(max_length=127)
    phone = forms.CharField(min_length=11, max_length=11)
    iin = forms.CharField(min_length=12, max_length=12)
    name = forms.CharField(max_length=30)
    surname = forms.CharField(max_length=30)
    pass1 = forms.CharField(min_length=8)
    pass2 = forms.CharField(min_length=8)

