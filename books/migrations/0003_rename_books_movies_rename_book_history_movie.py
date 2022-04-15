# Generated by Django 4.0.2 on 2022-04-03 11:28

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('books', '0002_rename_authors_books_cast_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Books',
            new_name='Movies',
        ),
        migrations.RenameField(
            model_name='history',
            old_name='book',
            new_name='movie',
        ),
    ]
