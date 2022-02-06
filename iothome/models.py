from django.db import models

class Registration(models.Model):
    username=models.CharField(max_length=20)
    name=models.CharField(max_length=50)
    email=models.EmailField(primary_key=True)
    password=models.CharField(max_length=50)
    is_active=models.BooleanField(default=False)
