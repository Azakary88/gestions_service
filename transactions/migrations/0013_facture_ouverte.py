# Generated by Django 4.2.17 on 2024-12-23 18:47

from django.db import migrations, models



class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0012_remove_transaction_facture_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='facture',
            name='ouverte',
            field=models.DateField(default="2024-12-24"),

        ),
    ]