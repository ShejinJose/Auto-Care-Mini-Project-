from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, UserDetails

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'role', 'password1', 'password2')

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Email')

class UserDetailsForm(forms.ModelForm):
    class Meta:
        model = UserDetails
        fields = ['name', 'phone', 'address', 'city', 'place', 'pincode']