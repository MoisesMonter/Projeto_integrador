# Generated by Django 4.1.5 on 2023-01-06 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0034_alter_generated_election_ativo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='election',
            name='Data',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]