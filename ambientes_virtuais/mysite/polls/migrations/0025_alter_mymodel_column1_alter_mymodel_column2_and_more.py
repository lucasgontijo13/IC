# Generated by Django 5.0.7 on 2024-08-06 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0024_alter_mymodel_column1_alter_mymodel_column2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mymodel',
            name='column1',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='mymodel',
            name='column2',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='mymodel',
            name='column3',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='mymodel',
            name='column4',
            field=models.TextField(default='Valor padrão'),
        ),
    ]
