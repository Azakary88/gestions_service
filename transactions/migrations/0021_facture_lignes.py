# Generated by Django 4.2.17 on 2024-12-31 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0020_remove_facture_lignes'),
    ]

    operations = [
        migrations.AddField(
            model_name='facture',
            name='lignes',
            field=models.ManyToManyField(related_name='factures_associees', to='transactions.lignefacture'),
        ),
    ]
