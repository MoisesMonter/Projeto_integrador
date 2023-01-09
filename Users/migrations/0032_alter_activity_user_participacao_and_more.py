# Generated by Django 4.1.5 on 2023-01-06 14:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0031_generated_election'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity_user',
            name='Participacao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.generated_election'),
        ),
        migrations.AlterField(
            model_name='data_election',
            name='N_Eleicao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.generated_election'),
        ),
        migrations.AlterField(
            model_name='interaction_user',
            name='N_Eleicao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.generated_election'),
        ),
    ]