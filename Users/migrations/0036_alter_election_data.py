# Generated by Django 4.1.5 on 2023-01-06 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0035_alter_election_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='election',
            name='Data',
            field=models.DateField(null=True),
        ),
    ]
