from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Login(AbstractUser):
    userType = models.CharField(max_length=100)
    viewPass = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.username


class UserRegistration(models.Model):
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    phone = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=300, null=True)
    image = models.ImageField(null=True, upload_to="profile")
    loginid = models.ForeignKey(Login, on_delete=models.CASCADE, null=True)


    def __str__(self):
        return self.name


class Feedback(models.Model):
    uid=models.ForeignKey(UserRegistration, on_delete=models.CASCADE, null=True)
    subject = models.CharField(max_length=100, null=True)
    feedback=models.CharField(max_length=300, null=True)
    reply=models.CharField(max_length=300, null=True)