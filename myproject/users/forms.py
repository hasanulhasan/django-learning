from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Permission, Group
from django import forms
import re
from django.contrib.auth.forms import AuthenticationForm

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

    # field errors
    def clean_password1(self):
            password1 = self.cleaned_data.get('password1')
            pattern = re.compile(
                        r'^(?=.*[A-Z])'       # at least one uppercase
                        r'(?=.*[a-z])'        # at least one lowercase
                        r'(?=.*\d)'           # at least one digit
                        r'(?=.*[@$!%*?&])'    # at least one special character
                        r'[A-Za-z\d@$!%*?&]$'  # allowed chars & min length 8
                    )
            if not password1:
                raise forms.ValidationError("Password is required")
            if len(password1) < 8:
                raise forms.ValidationError("Password must be at least 8 characters long")
            # if not pattern.match(password1):
            #     raise forms.ValidationError(
            #         "Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character."
            #     )
            return password1
    
    # non field errors
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        confirm_password = cleaned_data.get("confirm_password")

        if password1 and confirm_password and password1 != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        
        return cleaned_data
    
class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class AssignedRoleForm(forms.Form):
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label="Select a role",
    )

class CreateGroupForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Assign Permissions"
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']