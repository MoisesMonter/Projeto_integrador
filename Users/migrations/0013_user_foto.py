# Generated by Django 4.1.5 on 2023-01-04 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0012_user_foto_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='Foto',
            field=models.ImageField(default=1, upload_to='BD_User_img/', verbose_name='Imagem do perfil'),
            preserve_default=False,
        ),
    ]
