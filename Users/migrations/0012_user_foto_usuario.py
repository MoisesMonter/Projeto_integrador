# Generated by Django 4.1.5 on 2023-01-04 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0011_remove_user_foto'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='Foto_Usuario',
            field=models.ImageField(default=1, upload_to='<django.db.models.fields.CharField>/', verbose_name='Imagem do perfil'),
            preserve_default=False,
        ),
    ]
