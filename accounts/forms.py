from django  import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from django.contrib.auth.forms import PasswordChangeForm

# Form for requesting a password reset (email input)
class ResetPasswordForm(forms.Form):
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}))

# Form for setting a new password
class NewPasswordForm(forms.Form):
    password = forms.CharField(label="New Password", widget=forms.PasswordInput(attrs={'placeholder': 'Enter your new password'}))
    confirm_password = forms.CharField(label="Confirm New Password", widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your new password'}))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("The two password fields must match.")
        return cleaned_data


class RegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Enter email address", "class": "form-control"}))
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter username", "class": "form-control"}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"placeholder": "Enter password", "class": "form-control"}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={"placeholder": "Confirm password", "class": "form-control"}))
    mobile_number = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Enter mobile number", "class": "form-control"}),
        label="Mobile Number",
    )

    class Meta:
        model = get_user_model()
        fields = ["email", "username", "password1", "password2", "mobile_number"]
    
    def clean_mobile_number(self):
        mobile_number = self.cleaned_data.get('mobile_number')
        if mobile_number:
            # Ensure that the phone number is in a valid format
            if len(mobile_number) < 10 or len(mobile_number) > 15:
                raise forms.ValidationError("Please enter a valid mobile number.")
        return mobile_number