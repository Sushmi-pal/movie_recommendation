# Book Recommender
With the Book Recommender app, you can view personalized recommendations based on your favorite categories chosen
        during registration and previously read books.

Features:
- Recommends the reader on the basis of the category of the books they like which is given to choose during registration.

There is CRUD operations on user, profile and books.
User creation is done by Django default User. In other to change some field which is not on default side, you have to make custom User model. Since here is no any required fields other than default user, default user model is used.
Profile and user have the relation of OneToOne Field.
Recommended books is added on recently added section based on the users choice of category.

##Installation
- You should have python, Django installed on your system.
- Run the command to install all the requirements.
```
pip install -r requirements.txt
```
- Run the command
```
python3 manage.py makemigrations
python3 manage.py migrate
```
- There is a file named category_data.py on the root directory. You have to run that code on the python shell at first. The steps are given there. The categories are added to table named Category from this code.
- Finally run the command to run the server.
```
python3 manage.py runserver
```