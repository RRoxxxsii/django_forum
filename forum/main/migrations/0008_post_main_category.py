# Generated by Django 4.2 on 2023-04-23 14:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_remove_post_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='main_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.blogcategory'),
        ),
    ]
