from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *


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



# class SlotForm(forms.ModelForm):
#     class Meta:
#         model = Slot
#         fields = ['slotname', 'mechanic', 'status']

# class SlotForm(forms.ModelForm):
#     class Meta:
#         model = Slot
#         fields = ['slotname', 'status', 'mechanic']  # Keep the mechanic field for now

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Limit the mechanic field queryset to service managers instead of mechanics
#         self.fields['mechanic'].queryset = CustomUser.objects.filter(role=UserRole.SERVICE_MANAGER)
#         self.fields['mechanic'].label = "Service Manager"  # Change the label to reflect this is for managers





class AllocateManagerForm(forms.ModelForm):
    class Meta:
        model = AllocatedManager
        fields = ['manager']  # Only the manager field

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Limit the queryset to only service managers
        self.fields['manager'].queryset = CustomUser.objects.filter(role=UserRole.SERVICE_MANAGER)



class SlotForm(forms.ModelForm):
    manager = forms.ModelChoiceField(queryset=CustomUser.objects.filter(role=UserRole.SERVICE_MANAGER), label="Service Manager")

    class Meta:
        model = Slot
        fields = ['slotname', 'status']

    def save(self, commit=True):
        # Save the slot first
        slot = super().save(commit=False)

        # Save the slot instance
        if commit:
            slot.save()

        # Handle the allocated manager assignment
        manager = self.cleaned_data.get('manager')
        if manager:
            AllocatedManager.objects.update_or_create(
                slot=slot,
                defaults={'manager': manager}
            )
        return slot
class ManagerAllocationForm(forms.Form):
    manager = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(role=UserRole.SERVICE_MANAGER),
        label="Service Manager",
        required=True
    )