# Generated by Django 5.0.7 on 2024-08-07 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0036_remove_mymodel_cis_control_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='mymodel',
            name='column5',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='mymodel',
            name='column6',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='mymodel',
            name='column7',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='mymodel',
            name='column8',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='mymodel',
            name='action',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='mymodel',
            name='column1',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='mymodel',
            name='column2',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='mymodel',
            name='column3',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='mymodel',
            name='column4',
            field=models.CharField(default='', max_length=200),
        ),
    ]
