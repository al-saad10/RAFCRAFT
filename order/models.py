from django.contrib.auth.models import User
from products.models import  Product
from django.db import models
from django.core.validators import MinValueValidator
import uuid

#cart models
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Allow for both logged-in and guest users
    guest_session_id = models.CharField(max_length=255, null=True, blank=True)  # Optional guest session ID
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price


#order models
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    guest_session_id = models.CharField(max_length=255, null=True, blank=True, default=uuid.uuid4().hex)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    address = models.TextField(max_length=1000)
    country = models.CharField(max_length=50)
    company = models.CharField(max_length=50,null=True, blank=True,)
    city = models.CharField(max_length=50)
    order_note = models.CharField(max_length=1000, blank=True)
    

    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def __str__(self):
        return self.full_name()
    
class OrderItem(models.Model):
    STATUS_CHOICES = (
        ('Order Pending', 'Order Pending'),
        ('Accepted', 'Accepted'),
        ('Packed', 'Packed'),
        ('On The Way', 'On The Way'),
        ('Delivered', 'Delivered'),
        ('Cancel', 'Cancel'),
    )

    DEFAULT_STATUS = 'Order pending'

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    product_price = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=DEFAULT_STATUS)  # Set default status

    def sub_total(self):
        return self.quantity * self.product_price

    def __str__(self):
        return self.product.name