# Generated by Django 2.1.3 on 2018-12-12 22:41

from django.db import migrations
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modulepage',
            name='goals',
            field=wagtail.core.fields.RichTextField(),
        ),
    ]
