# Generated by Django 4.1.5 on 2023-01-05 10:53

from django.db import migrations
import stdimage.models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0019_alter_user_imagem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='imagem',
            field=stdimage.models.JPEGField(force_min_size=False, upload_to='BD_User_img', variations={'thumbnail': (200, 200)}),
        ),
    ]
