# Generated by Django 4.2 on 2023-04-23 13:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_rename_subcategory_slug_subcategory_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.post', verbose_name='Родитель'),
        ),
    ]
