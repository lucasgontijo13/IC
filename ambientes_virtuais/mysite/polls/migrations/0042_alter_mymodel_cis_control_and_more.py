# Generated by Django 5.0.7 on 2024-08-07 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0041_remove_mymodel_action_remove_mymodel_column1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mymodel',
            name='cis_control',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='mymodel',
            name='cis_sub_control',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='mymodel',
            name='descricao',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='mymodel',
            name='funcao_de_seguranca',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='mymodel',
            name='nist_csf',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='mymodel',
            name='nome_da_subcategoria',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='mymodel',
            name='tipo_de_ativo',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='mymodel',
            name='titulo',
            field=models.CharField(max_length=255),
        ),
    ]
