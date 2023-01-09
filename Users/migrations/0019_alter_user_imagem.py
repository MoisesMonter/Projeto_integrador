# Generated by Django 4.1.5 on 2023-01-05 10:51

from django.db import migrations
import stdimage.models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0018_rename_imagem_jpeg_user_imagem_alter_user_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='imagem',
            field=stdimage.models.JPEGField(force_min_size=False, upload_to='path/to/img', variations={'thumbnail': (100, 75)}),
        ),
    ]