# Generated by Django 5.0.7 on 2024-08-06 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0023_alter_mymodel_column1_alter_mymodel_column2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mymodel',
            name='column1',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='mymodel',
            name='column2',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='mymodel',
            name='column3',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='mymodel',
            name='column4',
            field=models.CharField(default='Valor padrão', max_length=1000),
        ),
    ]