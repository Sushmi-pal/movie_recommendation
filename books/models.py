from django.db import models
from user.models import Category
from django.contrib.auth.models import User


# Create your models here.


class Books(models.Model):
    name = models.CharField(max_length=100)
    authors = models.TextField()
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    info_user = models.ForeignKey(User, on_delete=models.CASCADE)
    book_image = models.ImageField(upload_to='book_pic')

class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
