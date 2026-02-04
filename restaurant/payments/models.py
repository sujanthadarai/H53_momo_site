from django.db import models
from django.contrib.auth.models import User
from core.models import Momo

# Create your models here.
class Transaction(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    product_code=models.CharField(max_length=200)
    transaction_uuid=models.CharField(max_length=200)
    transaction_code=models.CharField(max_length=200)
    total_amount=models.CharField(max_length=200)
    status=models.CharField(max_length=200)
    created_at=models.DateTimeField(auto_now=True)

class Order(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    transcation_uuid=models.CharField(max_length=200)
    status=models.CharField(max_length=200)
    created_at=models.DateTimeField(auto_now=True)
    
class OrderItem(models.Model):
    order=models.ForeignKey(Order, on_delete=models.CASCADE,related_name="items")
    momo=models.ForeignKey(Momo, on_delete=models.CASCADE)
    price=models.CharField(max_length=200)
    quantity=models.PositiveIntegerField()
    
    