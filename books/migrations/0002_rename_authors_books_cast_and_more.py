# Generated by Django 4.0.2 on 2022-04-03 08:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='books',
            old_name='authors',
            new_name='cast',
        ),
        migrations.RenameField(
            model_name='books',
            old_name='book_image',
            new_name='movie_image',
        ),
    ]
