from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .utils import validate_email_full


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            return email
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Этот email уже зарегистрирован.')
        valid, error_msg = validate_email_full(email)
        if not valid:
            raise forms.ValidationError(error_msg)
        return email
