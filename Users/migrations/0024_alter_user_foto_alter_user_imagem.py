# Generated by Django 4.1.5 on 2023-01-05 11:28

from django.db import migrations, models
import stdimage.models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0023_alter_user_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='Foto',
            field=models.ImageField(default='<django.db.models.fields.CharField>Img_Perfil.jpg', upload_to='BD_User_img', verbose_name='Imagem do perfil'),
        ),
        migrations.AlterField(
            model_name='user',
            name='imagem',
            field=stdimage.models.JPEGField(default='<django.db.models.fields.CharField>Img_Perfil.jpg', force_min_size=False, upload_to='BD_User_img', variations={'thumbnail': (200, 200)}, verbose_name='Foto de Perfil'),
        ),
    ]