# Generated by Django 5.0.7 on 2024-07-23 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0011_cliente_last_login'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]
