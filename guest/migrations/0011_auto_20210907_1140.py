# Generated by Django 3.2.4 on 2021-09-07 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guest', '0010_rename_water_suplly_addroommodel_water_supply'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addroommodel',
            name='washroom',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='addroommodel',
            name='water_supply',
            field=models.CharField(max_length=20),
        ),
    ]