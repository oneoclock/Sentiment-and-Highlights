# Generated by Django 2.0.4 on 2018-06-08 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0005_auto_20180608_1825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviews',
            name='intensity',
            field=models.FloatField(default=0),
        ),
    ]