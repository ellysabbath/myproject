# Generated by Django 5.1.5 on 2025-02-24 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_tithes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tithes',
            name='date',
            field=models.CharField(max_length=20),
        ),
    ]
