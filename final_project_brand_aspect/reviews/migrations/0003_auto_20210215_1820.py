# Generated by Django 2.2.6 on 2021-02-15 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20210215_1813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviews',
            name='review_text',
            field=models.TextField(max_length=850, null=True, unique=True),
        ),
    ]
