# Generated by Django 5.0.7 on 2024-08-06 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0032_remove_mymodel_data_mymodel_column1_mymodel_column2_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mymodel',
            name='column1',
        ),
        migrations.RemoveField(
            model_name='mymodel',
            name='column2',
        ),
        migrations.RemoveField(
            model_name='mymodel',
            name='column3',
        ),
        migrations.RemoveField(
            model_name='mymodel',
            name='column4',
        ),
        migrations.AddField(
            model_name='mymodel',
            name='data',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='mymodel',
            name='action',
            field=models.CharField(default='NÃ£o se aplica', max_length=20),
        ),
    ]
