from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Works(models.Model):
    title = models.CharField(max_length=10)
    image = models.ImageField(upload_to='images/images')
    desc = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Category(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name

	
	class Meta:
		verbose_name_plural = 'categories' 


class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)
    is_owner = models.BooleanField(default=False)



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    full_name = models.CharField(max_length=20, blank=True, null=True)
    phone_number = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.user.username

class Vehicles(models.Model):
    vehicle_model = models.CharField(max_length=100)
    rent_price = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=250, default='', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/product/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_vehicles')
    rented_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='rented_vehicles')
    isDelete = models.BooleanField(default=False)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.vehicle_model



class RentTransaction(models.Model):
    vehicle = models.ForeignKey(Vehicles, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100)
    amount = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_rented = models.DateTimeField(auto_now_add=True)
	
    def __str__(self):
          return self.transaction_id


class Review(models.Model):
    vehicle = models.ForeignKey(Vehicles, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.vehicle.vehicle_model}'