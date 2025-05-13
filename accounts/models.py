from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.TextField(max_length=10)
    major = models.TextField(null=True, max_length=30)
    mbti = models.CharField(null=True,max_length=4)
    age = models.IntegerField(null=True)
