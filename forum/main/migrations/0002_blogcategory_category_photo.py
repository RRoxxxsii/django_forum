# Generated by Django 4.2 on 2023-04-19 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogcategory',
            name='category_photo',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]