# Generated by Django 5.0.7 on 2024-07-23 21:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0015_token'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Token',
        ),
    ]
