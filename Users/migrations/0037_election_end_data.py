# Generated by Django 4.1.5 on 2023-01-06 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0036_alter_election_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='election',
            name='End_Data',
            field=models.DateField(null=True),
        ),
    ]
