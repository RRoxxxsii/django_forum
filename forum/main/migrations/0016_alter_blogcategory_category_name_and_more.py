# Generated by Django 4.2 on 2023-05-18 09:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0015_feedback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogcategory',
            name='category_name',
            field=models.CharField(max_length=255, unique=True, verbose_name='Название категории'),
        ),
        migrations.AlterField(
            model_name='blogcategory',
            name='category_photo',
            field=models.ImageField(blank=True, upload_to='', verbose_name='Изображение категории'),
        ),
        migrations.AlterField(
            model_name='blogcategory',
            name='slug',
            field=models.SlugField(max_length=255, unique=True, verbose_name='Слаг категории'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='text',
            field=models.TextField(verbose_name='Текст обратной связи'),
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Внешний ключ автора'),
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.subcategory', verbose_name='Внешний ключ подкатегории'),
        ),
        migrations.AlterField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Время публикации поста'),
        ),
        migrations.AlterField(
            model_name='post',
            name='is_published',
            field=models.BooleanField(default=True, help_text='Опубликован ли пост', verbose_name='Опубликован'),
        ),
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.TextField(verbose_name='Пост'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Заголовок поста'),
        ),
        migrations.AlterField(
            model_name='post',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Время редактирования'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.blogcategory', verbose_name='Внешний ключ категории'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='slug',
            field=models.SlugField(max_length=255, verbose_name='Слаг подкатегории'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='sub_category_name',
            field=models.CharField(max_length=255, verbose_name='Название подкатегории'),
        ),
    ]