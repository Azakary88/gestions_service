# Generated by Django 4.2.17 on 2024-12-22 17:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0006_rename_prix_total_lignefacture_montant'),
    ]

    operations = [
        migrations.AddField(
            model_name='lignefacture',
            name='transaction',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='transactions.transaction'),
            preserve_default=False,
        ),
    ]
