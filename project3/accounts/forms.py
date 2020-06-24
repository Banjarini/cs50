from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

# Sign Up Form
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address')
    class Meta:
        model = User
        fields = [
            'email',
            'username', 
            'first_name', 
            'last_name', 
            ]