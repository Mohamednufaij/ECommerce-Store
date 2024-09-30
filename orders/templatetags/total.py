from django import template

register = template.Library()

@register.simple_tag(name='total')
def total(cart):
    total = 0  # Initialize the total variable
    for item in cart.ordered_items.all():  # Use 'ordered_items' instead of 'added_items'
        total += item.quantity * item.product.price
    return total

