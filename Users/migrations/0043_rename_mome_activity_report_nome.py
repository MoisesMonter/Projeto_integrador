# Generated by Django 4.1.5 on 2023-01-11 15:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0042_rename_balao_activity_report_balao_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activity_report',
            old_name='mome',
            new_name='nome',
        ),
    ]