# Generated by Django 4.1.5 on 2023-01-06 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0029_remove_user_imagem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='election',
            name='N_Eleicao',
            field=models.IntegerField(auto_created=True, primary_key=True, serialize=False, unique=True),
        ),
    ]
