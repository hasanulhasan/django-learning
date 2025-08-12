from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
import re

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldName in ['username', 'password1', 'password2']:
            self.fields[fieldName].help_text = None

class CustomRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name','last_name', 'email', 'password1', 'confirm_password')

    def clean_password1(self):
            password1 = self.cleaned_data.get('password1')
            pattern = re.compile(
                        r'^(?=.*[A-Z])'       # at least one uppercase
                        r'(?=.*[a-z])'        # at least one lowercase
                        r'(?=.*\d)'           # at least one digit
                        r'(?=.*[@$!%*?&])'    # at least one special character
                        r'[A-Za-z\d@$!%*?&]{8,}$'  # allowed chars & min length 8
                    )
            if not password1:
                raise forms.ValidationError("Password is required")
            if len(password1) < 8:
                raise forms.ValidationError("Password must be at least 8 characters long")
            if not pattern.match(password1):
                raise forms.ValidationError(
                    "Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character."
                )
            return password1