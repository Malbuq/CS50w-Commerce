# Generated by Django 5.0 on 2023-12-28 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='description',
            field=models.TextField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='listing',
            name='imageURl',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]
