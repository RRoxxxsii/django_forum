# Generated by Django 4.2 on 2023-04-24 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_subcategory_last_post_author_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subcategory',
            name='last_post_date',
            field=models.DateTimeField(blank=True, db_column='last_post_date', null=True),
        ),
    ]