# Generated by Django 4.1.5 on 2023-01-04 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0014_remove_user_foto_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='Foto',
            field=models.ImageField(default=None, upload_to='BD_User_img/', verbose_name='Imagem do perfil'),
        ),
    ]
