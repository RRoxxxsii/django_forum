# Generated by Django 4.2 on 2023-04-19 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='country',
            options={'ordering': ('country',), 'verbose_name': 'Страна', 'verbose_name_plural': 'Страны'},
        ),
        migrations.AlterField(
            model_name='author',
            name='profile_photo',
            field=models.ImageField(blank=True, help_text='Фото профиля', upload_to='photos/%Y/%m/%d/'),
        ),
    ]
