from django.db import models

# Create your models here.
class FollowerCount(models.Model):
    follower = models.CharField(max_length=200)
    user = models.CharField(max_length=200)
    
    def __str__(self):
        return f'{self.follower}-following-{self.user}'


