# Generated by Django 4.2.17 on 2024-12-30 21:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0018_facture__updating_total'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProduitService',
        ),
        migrations.AddField(
            model_name='lignefacture',
            name='facture',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='lignes_facture', to='transactions.facture'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='facture',
            name='lignes',
            field=models.ManyToManyField(related_name='factures_associees', to='transactions.lignefacture'),
        ),
    ]
