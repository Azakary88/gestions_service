# Generated by Django 4.2.17 on 2024-12-23 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0010_transaction_facture'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='ouverte',
            field=models.BooleanField(default=True),
        ),
    ]