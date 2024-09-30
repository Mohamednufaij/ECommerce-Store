
from django import template

register = template.Library()

@register.simple_tag(name='get_status')
def get_status(status):
    # Ensure the status is within valid range
    status_array = ['confirmed', 'processed', 'delivered', 'rejected']
    
    # Safeguard against invalid status values
    if 0 <= status - 1 < len(status_array):
        return status_array[status - 1]
    else:
        return 'Unknown status'  # Return a default value if status is invalid
