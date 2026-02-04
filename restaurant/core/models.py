from django.db import models

# Create your models here.

class Contact(models.Model):
    name=models.CharField(max_length=200)
    email=models.EmailField()
    phone=models.CharField(max_length=20)
    message=models.TextField()
    
class Category(models.Model):
    title=models.CharField(max_length=200)
    
    def __str__(self):
        return self.title
    
class Momo(models.Model):
    name=models.CharField(max_length=200) #veg steam momo
    category=models.ForeignKey(Category, on_delete=models.CASCADE) #
    desc=models.TextField(blank=True)
    mark_price=models.DecimalField(max_digits=8,decimal_places=2,default=0) #100
    discount_percent=models.DecimalField(max_digits=4,decimal_places=2,default=0) #10
    price=models.DecimalField(max_digits=8,decimal_places=2,editable=False)#90
    image=models.ImageField(upload_to="images")
    
    # mark_price *(1-discount_percent/100) ==> 100 (1-0.1) ==>100 *0.9 ==>90
    
    def __str__(self):
        return self.name
    
    def save(self,*args, **kwargs):
        self.price=self.mark_price*(1-self.discount_percent/100)
        super().save(*args, **kwargs)
        
    
    
    
class Testemonial(models.Model):
    name=models.CharField(max_length=200)
    image=models.ImageField(upload_to="testemonial_images")
    message=models.TextField()
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    