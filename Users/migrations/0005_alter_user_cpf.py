# Generated by Django 4.1.5 on 2023-01-04 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0004_alter_user_id_academico'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='CPF',
            field=models.CharField(max_length=11, unique=True),
        ),
    ]
