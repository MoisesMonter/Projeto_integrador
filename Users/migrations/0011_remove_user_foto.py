# Generated by Django 4.1.5 on 2023-01-04 20:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0010_alter_user_foto'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='Foto',
        ),
    ]
