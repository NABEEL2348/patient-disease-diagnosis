from django.db import models

# Create your models here.
class RegisterDataset(models.Model):
    Name = models.CharField(max_length=20)
    Email = models.CharField(max_length=30)
    Password = models.CharField(max_length=20)
