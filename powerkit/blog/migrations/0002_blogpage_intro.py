# Generated by Django 2.1.3 on 2018-12-05 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpage',
            name='intro',
            field=models.TextField(blank=True, null=True),
        ),
    ]
