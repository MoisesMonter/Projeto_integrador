# Generated by Django 4.1.5 on 2023-01-04 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0007_alter_user_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='Foto',
            field=models.ImageField(upload_to='BD_User_img/<django.db.models.fields.CharField>/', verbose_name='Imagem do perfil'),
        ),
    ]