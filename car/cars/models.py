from django.db import models
from django.contrib.auth.models import User

class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=30,unique=True)
    phone = models.IntegerField(unique=True)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username

class Car(models.Model):
    model = models.CharField(max_length=20)
    year = models.IntegerField()
    color = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to="car_images", unique=True)

    def __str__(self):
        return self.model

class Book(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = models.TextField()

    def __str__(self):
        return f"{self.user.user.username} booked {self.car.model}"
        
class Feedback(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    feedback = models.TextField()

    def __str__(self):
        return f"Feedback from {self.user.user.username}"