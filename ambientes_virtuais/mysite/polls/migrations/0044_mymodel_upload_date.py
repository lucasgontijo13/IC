# Generated by Django 5.0.7 on 2024-08-12 18:18

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0043_planilhaupload'),
    ]

    operations = [
        migrations.AddField(
            model_name='mymodel',
            name='upload_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]