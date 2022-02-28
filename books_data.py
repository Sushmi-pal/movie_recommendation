import pandas as pd
from django.contrib.auth.models import User

from books.models import Books
from user.models import Category
import random

book_data = pd.read_csv("/home/dell/Desktop/book_recommender/book_recommendation/book_models.csv")

for row_data in range(len(book_data)):
    cat_id = Category.objects.filter(name=book_data.iloc[row_data]['Genres'])

    users_id_list = list(User.objects.all())

    user_id = random.choice(users_id_list)

    Books.objects.create(name=book_data.iloc[row_data]['Book Title'],
                         authors=book_data.iloc[row_data]['Book Author'],
                         description=book_data.iloc[row_data]['Summary'],
                         category= cat_id,
                         info_user=user_id)