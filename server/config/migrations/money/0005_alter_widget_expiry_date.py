# Generated by Django 3.2.2 on 2021-08-18 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0004_widget_expiry_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='widget',
            name='expiry_date',
            field=models.DateTimeField(verbose_name='Дата окончания цели'),
        ),
    ]
