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
        widgets = {
            'address': forms.Textarea(attrs={'rows': 2}),
        }

# class VehicleForm(forms.ModelForm):
#     class Meta:
#         model = Vehicle
#         fields = ['vehicle_type', 'vehicle_brand', 'vehicle_variant', 'vehicle_number']
#         widgets = {
#             'vehicle_type': forms.Select(attrs={'id': 'vehicleType', 'required': True}),
#             'vehicle_brand': forms.Select(attrs={'id': 'vehicleBrand', 'required': True}),
#             'vehicle_variant': forms.TextInput(attrs={'id': 'vehicleVariant', 'required': True}),
#             'vehicle_number': forms.TextInput(attrs={'id': 'vehicleNumber', 'required': True}),
#         }


from .models import VehicleMake, VehicleModel

class VehicleMakeForm(forms.ModelForm):
    class Meta:
        model = VehicleMake
        fields = ['name', 'image']  # Define the fields to include in the form

class VehicleModelForm(forms.ModelForm):
    class Meta:
        model = VehicleModel
        fields = ['model_name', 'year', 'image', 'vehicle_type'] 

        # Customize widgets (optional) for better rendering
        widgets = {
            'vehicle_type': forms.RadioSelect,  # To show radio buttons for vehicle type choices
        }
