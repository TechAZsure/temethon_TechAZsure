from django import forms
from .models import BankBranch

class BankBranchRegistrationForm(forms.ModelForm):
    class Meta:
        model = BankBranch
        fields = ['bank_name', 'branch_name', 'manager_name', 'email', 'branch_code', 'contact_number', 'password']

    password = forms.CharField(widget=forms.PasswordInput)

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()

class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
