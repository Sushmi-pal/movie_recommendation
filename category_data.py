# Run this in python shell
# Run "python3 manage.py shell" and then write this line one by one so that the data inside Category table will be populated
from user.models import Category

categories = ['Horror',
              'Thriller',
              'Young adult literature',
              'Adventure novel',
              'Satire',
              'Biography',
              'Dystopia',
              'Gothic fiction',
              'Autobiography',
              'Alternate history']

for category in categories:
    Category.objects.create(name=category)
