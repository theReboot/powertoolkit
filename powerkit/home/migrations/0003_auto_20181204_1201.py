# Generated by Django 2.1.3 on 2018-12-04 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20181204_1159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='intro',
            field=models.TextField(blank=True),
        ),
    ]