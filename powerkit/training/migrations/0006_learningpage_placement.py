# Generated by Django 2.1.3 on 2019-01-05 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0005_auto_20190103_1159'),
    ]

    operations = [
        migrations.AddField(
            model_name='learningpage',
            name='placement',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
