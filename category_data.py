# Run this in python shell
# Run "python3 manage.py shell" and then write this line one by one so that the data inside Category table will be populated
from user.models import Category

categories = ['Fiction',
              'Speculative fiction',
              'Science Fiction',
              'Novel',
              'Fantasy',
              'Childrens literature',
              'Mystery',
              'Suspense',
              'Historical novel',
              'Crime Fiction',
              'Horror',
              'Historical fiction',
              'Romance novel',
              'Thriller',
              'Young adult literature',
              'Dystopia',
              'Detective fiction',
              'Non-fiction',
              'Spy fiction',
              'Satire',
              'Adventure novel',
              'Alternate history',
              'Autobiography',
              'Gothic fiction',
              'Biography']
for category in categories:
    Category.objects.create(name=category)
