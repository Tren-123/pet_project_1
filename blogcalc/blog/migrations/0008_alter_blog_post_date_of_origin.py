# Generated by Django 4.1 on 2022-08-29 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_blog_post_date_of_origin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog_post',
            name='date_of_origin',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
