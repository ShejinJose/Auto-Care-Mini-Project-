from django import template
from ..models import Vehicle

register = template.Library()

@register.filter
def get_selected_vehicle(vehicles, selected_vehicle_id):
    try:
        return Vehicle.objects.get(id=selected_vehicle_id)
    except Vehicle.DoesNotExist:
        return None
