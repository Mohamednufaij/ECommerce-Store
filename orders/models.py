# from django.db import models
# from customers.models import Customer
# from products.models import Product
# class Order(models.Model):
#     LIVE=1
#     DELETE=0
#     DELETE_CHOICES=((LIVE,'Live'),(DELETE,'Delete'))
#     CART_STAGE=0
#     ORDER_CONFIRMED=1
#     ORDER_PROCESSED=2
#     ORDER_DELIVERED=3
#     ORDER_REJECTED=4
#     STATUS_CHOICE=((ORDER_PROCESSED,"ORDER_PROCESSED"),
#                    (ORDER_CONFIRMED,"ORDER_CONFIRMED"),
#                    (ORDER_REJECTED,"ORDER_REJECTED"))
#     order_status=models.IntegerField(choices=STATUS_CHOICE,default=CART_STAGE)
#     owner=models.ForeignKey(Customer,related_name='orders',on_delete=models.SET_NULL,null=True)
#     delete_status=models.IntegerField(choices=DELETE_CHOICES,default=LIVE)
#     created_at=models.DateTimeField(auto_now_add=True)
#     updated_at=models.DateTimeField(auto_now=True)
# class Ordered_item(models.Model):
#     product=models.ForeignKey(Product,related_name='added_cart',on_delete=models.SET_NULL,null=True)
#     quantity=models.IntegerField(default=1)
#     orders=models.ForeignKey(Order,related_name='ordered_items',on_delete=models.CASCADE)

# def __str__(self) -> str:
#         return "order-{}-{}".format(self.id,self.owner.name)


from django.db import models
from customers.models import Customer
from products.models import Product
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from customers.models import Customer

class Order(models.Model):
    LIVE = 1
    DELETE = 0
    DELETE_CHOICES = ((LIVE, 'Live'), (DELETE, 'Delete'))

    CART_STAGE = 0
    ORDER_CONFIRMED = 1
    ORDER_PROCESSED = 2
    ORDER_DELIVERED = 3
    ORDER_REJECTED = 4
    STATUS_CHOICE = (
        (ORDER_PROCESSED, "ORDER_PROCESSED"),
        (ORDER_CONFIRMED, "ORDER_CONFIRMED"),
        (ORDER_REJECTED, "ORDER_REJECTED"),
    )

    order_status = models.IntegerField(choices=STATUS_CHOICE, default=CART_STAGE)
    owner = models.ForeignKey(Customer, related_name='orders', on_delete=models.SET_NULL, null=True)
    delete_status = models.IntegerField(choices=DELETE_CHOICES, default=LIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_price = models.FloatField(default=0.0)  # Add this line

    def __str__(self):
        return "order-{}-{}".format(self.id, self.owner.name)  # Correct indentation

class Ordered_item(models.Model):
    product = models.ForeignKey(Product, related_name='added_cart', on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)
    orders = models.ForeignKey(Order, related_name='ordered_items', on_delete=models.CASCADE)

    def __str__(self):
        return f"Ordered item - {self.id} - {self.product.name}"  # Optional, for better representation


@receiver(post_save, sender=User)
def create_customer_profile(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_customer_profile(sender, instance, **kwargs):
    instance.customer_profile.save()