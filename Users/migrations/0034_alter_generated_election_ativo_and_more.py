# Generated by Django 4.1.5 on 2023-01-06 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0033_alter_generated_election_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generated_election',
            name='Ativo',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='generated_election',
            name='Disponibilizar',
            field=models.BooleanField(null=True),
        ),
    ]