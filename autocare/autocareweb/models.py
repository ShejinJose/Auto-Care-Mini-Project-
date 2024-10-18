from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

class UserRole(models.TextChoices):
    ADMIN = 'admin', _('Admin')
    SERVICE_MANAGER = 'service_manager', _('ServiceManager')
    MECHANIC = 'mechanic', _('Mechanic')
    CUSTOMER = 'customer', _('Customer')

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=UserRole.choices, default=UserRole.CUSTOMER)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class UserDetails(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='details')
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=50)
    place = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)

    def __str__(self):
        return self.name

####//////////Vehicle details//////////////////
# class Vehicle(models.Model):
#     VEHICLE_TYPE_CHOICES = [
#         ('car', 'Car'),
#         ('bike', 'Bike'),
#         # Add more types if needed
#     ]

#     owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='vehicles')
#     vehicle_type = models.CharField(max_length=10, choices=VEHICLE_TYPE_CHOICES)
#     vehicle_brand = models.CharField(max_length=50)
#     vehicle_variant = models.CharField(max_length=50)
#     vehicle_number = models.CharField(max_length=20, unique=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.vehicle_type}{self.vehicle_brand} {self.vehicle_variant} ({self.vehicle_number})"
    
VEHICLE_TYPE_CHOICES = [
    ('car', 'Car'),
    ('bike', 'Bike'),
]

class VehicleMake(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='vehicle_make_images/', blank=True, null=True)

    def __str__(self):  
        return self.name

class VehicleModel(models.Model):
    make = models.ForeignKey(VehicleMake, on_delete=models.CASCADE)
    model_name = models.CharField(max_length=100)
    year = models.IntegerField()
    image = models.ImageField(upload_to='vehicle_model_images/', blank=True, null=True)
    vehicle_type = models.CharField(max_length=10, choices=VEHICLE_TYPE_CHOICES)

    def _str_(self):
        return f"{self.make.name} {self.model_name} ({self.year}) - {self.get_vehicle_type_display()}"
    


class Vehicle(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    vehicle_model = models.ForeignKey(VehicleModel, on_delete=models.CASCADE)
    registration_number = models.CharField(max_length=20, unique=True)



#////////////////Service Lists//////////////



class ServiceCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='service_category_images/', blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return self.name
    

class ServiceType(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(ServiceCategory, related_name='service_types', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='service_type_images/', blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class ServicePrice(models.Model):
    service_type = models.ForeignKey(ServiceType, related_name='service_prices', on_delete=models.CASCADE)
    vehicle_model = models.ForeignKey(VehicleModel, related_name='service_prices', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    def _str_(self):
        return f"{self.service_type.name} for {self.vehicle_model} - ₹{self.price} INR"
    

#///////////////// Service cart ///////////////////////////
class ServiceCart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # User who owns the cart
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)  # Service type added to the cart
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)  # Selected vehicle
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart: {self.user.email} - {self.service_type.name} for {self.vehicle.registration_number}"
    


#//////////////////////////  slot list ////////////////////////

class SlotStatus(models.TextChoices):
    ALLOCATED = 'allocated', _('Allocated')
    FREE = 'free', _('Free')
    DISABLED = 'disabled', _('Disabled')

class Slot(models.Model):
    slotname = models.CharField(max_length=100)
    mechanic = models.ForeignKey(CustomUser, limit_choices_to={'role': 'mechanic'}, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=10, choices=SlotStatus.choices, default=SlotStatus.FREE)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.slotname)
        super(Slot, self).save(*args, **kwargs)

class AllocatedManager(models.Model):
    manager = models.ForeignKey(
        CustomUser,
        limit_choices_to={'role': UserRole.SERVICE_MANAGER},
        on_delete=models.CASCADE
    )
    slot = models.ForeignKey(
        Slot,
        on_delete=models.CASCADE
    )


class AllocatedMechanic(models.Model):
    mechanic = models.ForeignKey(
        CustomUser,
        limit_choices_to={'role': UserRole.MECHANIC},
        on_delete=models.CASCADE,
        related_name='allocated_mechanics'  # Unique reverse accessor for mechanic
    )
    manager = models.ForeignKey(
        CustomUser,
        limit_choices_to={'role': UserRole.SERVICE_MANAGER},
        on_delete=models.CASCADE,
        related_name='allocated_managers'  # Unique reverse accessor for manager
    )
    slot = models.ForeignKey(
        Slot,
        on_delete=models.CASCADE
    )
    allocated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('slot', 'mechanic')  # To prevent multiple mechanics being assigned to one slot

    def __str__(self):
        return f"Mechanic {self.mechanic.email} assigned to Slot {self.slot.slotname}"



from django.db import models
from django.utils.translation import gettext_lazy as _


class MechanicLevel(models.IntegerChoices):
    SENIOR = 1, _('Senior Level')
    MEDIUM = 2, _('Medium Level')
    ENTRY = 3, _('Entry Level')

class MechanicStatus(models.IntegerChoices):
    WORKING = 1, _('Working')
    ACTIVE = 2, _('Active')
    ABSENTEES = 3, _('Absentees')

class Mechanic(models.Model):
    mechanic = models.OneToOneField(CustomUser, on_delete=models.CASCADE, default=1)
    status = models.IntegerField(choices=MechanicStatus.choices, default=MechanicStatus.ACTIVE)
    level = models.IntegerField(choices=MechanicLevel.choices, default=MechanicLevel.ENTRY)

    def __str__(self):
        return f"{self.userid.email} - {self.get_level_display()}"


