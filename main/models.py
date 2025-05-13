from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=50)
    writer = models.CharField(max_length=30)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    weather = models.CharField(max_length=20, default='맑음')
    content = models.TextField()
    pub_date = models.DateTimeField()
    image = models.ImageField(upload_to="post/", blank=True, null=True)

    def __str__(self):
        return self.title
    
    def summary(self):
        return self.content[:20]
    
