# Generated by Django 2.1.3 on 2018-12-18 08:41

from django.db import migrations
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('issue', '0003_issueindex'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issuepage',
            name='key_players',
            field=wagtail.core.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='issuepage',
            name='policy_background',
            field=wagtail.core.fields.RichTextField(blank=True, null=True),
        ),
    ]
