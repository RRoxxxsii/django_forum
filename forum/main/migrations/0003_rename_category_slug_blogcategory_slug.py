# Generated by Django 4.2 on 2023-04-19 15:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_blogcategory_category_photo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blogcategory',
            old_name='category_slug',
            new_name='slug',
        ),
    ]
