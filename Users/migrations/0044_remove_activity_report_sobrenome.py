# Generated by Django 4.1.5 on 2023-01-18 00:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0043_rename_mome_activity_report_nome'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity_report',
            name='sobrenome',
        ),
    ]