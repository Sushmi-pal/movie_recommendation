from django.db import models
from user.models import Category
from django.contrib.auth.models import User


# Create your models here.


class Books(models.Model):
    name = models.CharField(max_length=100)
    cast = models.TextField()
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    url = models.URLField(max_length=300)
    info_user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_image = models.ImageField(upload_to='movie_pic', default="movie_pic/default.png")

class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
