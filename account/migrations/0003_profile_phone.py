# Generated by Django 3.1.5 on 2021-01-25 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20210122_2237'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='phone',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]