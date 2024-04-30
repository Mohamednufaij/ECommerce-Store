from django import template

register = template.Library()

@register.simple_tag(name='total')
def total(cart):
    for item in cart.added_items.all():
        total+=item.quantity*item.product.price
    return total