# Generated by Django 4.2.17 on 2024-12-25 16:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0014_remove_lignefacture_facture_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facture',
            name='date_emission',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='facture',
            name='ouverte',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='date_emission',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
