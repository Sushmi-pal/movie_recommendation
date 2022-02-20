# Run this in python shell
# Run "python3 manage.py shell" and then write this line one by one so that the data inside Category table will be populated
from user.models import Category
categories = ['Biography', 'Children’s', 'Drama', 'Fairytale', 'Fantasy', 'History', 'Humor',
              'Horror', 'Mystery', 'Paranormal romance', 'Philosophy', 'Fiction', 'Suspense', 'Thriller']
for category in categories:
    Category.objects.create(name=category)