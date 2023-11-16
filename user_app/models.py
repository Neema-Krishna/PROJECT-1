from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class MyUser_registration(AbstractUser):
    user_type=models.CharField(max_length=20,null=True)
    # dob=models.DateField(null=True)
    phone=models.BigIntegerField(default=7320170541)
    
    
class Brand(models.Model):
    b_name=models.CharField(max_length=20)
    
    def __str__(self):
        return self.b_name
    
class Vehicle_name(models.Model):
    brand_name=models.ForeignKey(Brand,on_delete=models.CASCADE,related_name='brand_vehicles')
    v_name=models.CharField(max_length=40)
    
    def __str__(self):
        return self.v_name

class Vehicle(models.Model):
    name=models.ForeignKey(Vehicle_name,on_delete=models.CASCADE,related_name='vehicle_name_vehicles')
    # model=models.CharField(max_length=20)
    vin_number=models.IntegerField()
    image=models.ImageField(upload_to='images')
    image1=models.ImageField(upload_to='images',null=True,blank=True)
    image2=models.ImageField(upload_to='images',null=True,blank=True)
    image3=models.ImageField(upload_to='images',null=True,blank=True)
    description=models.CharField(max_length=100,null=True)
    year=models.IntegerField()
    price=models.IntegerField()
    gear_type=models.CharField(max_length=10,null=True)
    mileagae=models.CharField(max_length=10,null=True)
    power=models.CharField(max_length=10,null=True)
    # geartype=models.CharField(max_length=5,null=True)
    fueltype=models.CharField(max_length=10,null=True)
    kilometer=models.IntegerField(null=True)
    engine=models.CharField(max_length=10,null=True)
    color=models.CharField(max_length=10,null=True)
    created=models.DateTimeField(auto_now=True)
    updated=models.DateTimeField(auto_now=True)
    purpose=models.CharField(max_length=10,null=True)
    status=models.CharField(max_length=15,null=True)
    
    def __str__(self):
        return self.name.v_name
    
    
class Cart(models.Model):
    user=models.ForeignKey(MyUser_registration,on_delete=models.CASCADE,related_name='cart_user')
    vehicle_cart=models.ForeignKey(Vehicle,on_delete=models.CASCADE,related_name='cart_vehicle')
    def __str__(self):
        return self.vehicle_cart.name.v_name
    
class Booking(models.Model):
    user=models.ForeignKey(MyUser_registration,on_delete=models.CASCADE,related_name='booked_user')
    vehicle_booked=models.ForeignKey(Vehicle,on_delete=models.CASCADE,related_name='Booked_vehicle')
    date=models.DateField(auto_now=True)
    status=models.CharField(max_length=10)

class Query(models.Model):
    user=models.ForeignKey(MyUser_registration,on_delete=models.CASCADE,related_name='query_user')
    email=models.EmailField(null=True)
    subject=models.CharField(max_length=60)
    Your_question=models.CharField(max_length=60,null=True)
    datetime=models.DateField(auto_now=True)
    reply=models.CharField(max_length=60)
    
class Contact(models.Model):
    user=models.ForeignKey(MyUser_registration,on_delete=models.CASCADE,related_name='conatct_user')
    name=models.CharField(max_length=20) 
    phone=models.BigIntegerField()
    location=models.CharField(max_length=20)
    service=models.CharField(max_length=10)
    reply=models.CharField(max_length=30)   
    
class Information(models.Model):
    title=models.CharField(max_length=20)
    content=models.CharField(max_length=50)
    image=models.ImageField(upload_to='images',null=True)
    
class Payment(models.Model):
    user=models.ForeignKey(MyUser_registration,on_delete=models.CASCADE,related_name='payment_user')
    booking=models.ForeignKey(MyUser_registration,on_delete=models.CASCADE,related_name='payment_booking')
    datetime=models.DateTimeField(auto_now_add=True)
    
 

    
