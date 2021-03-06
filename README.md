# Book Recommender
With the Book Recommender app, you can view personalized recommendations based on your favorite categories chosen
        during registration and previously read books.

Features:
- Recommends the reader on the basis of the category of the books they like which is given to choose during registration.

There is CRUD operations on user, profile and books.
User creation is done by Django default User. In other to change some field which is not on default side, you have to make custom User model. Since here is no any required fields other than default user, default user model is used.
Profile and user have the relation of OneToOne Field.
Recommended books is added on recommended books section based on the viewed books. And the user who has written the description of a specific book can only update and delete that book detail.
You can change the password by clicking on forgot password button which is on Login Page.
## Installation
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
- Run the command
```
python3 manage.py shell
```
and inside that console write the command
```
exec(open('category_data.py').read())
```
- Finally run the command to run the server.
```
python3 manage.py runserver
```