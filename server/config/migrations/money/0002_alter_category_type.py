# Generated by Django 3.2.2 on 2021-08-11 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='type',
            field=models.CharField(choices=[('i', 'доход'), ('e', 'расход')], max_length=1, verbose_name='Тип'),
        ),
    ]
