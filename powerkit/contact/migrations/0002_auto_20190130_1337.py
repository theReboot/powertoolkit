# Generated by Django 2.1.5 on 2019-01-30 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailforms', '0003_capitalizeverbose'),
        ('wagtailcore', '0040_page_draft_title'),
        ('wagtailredirects', '0006_redirect_increase_max_length'),
        ('contact', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intro', models.TextField(blank=True)),
                ('email', models.CharField(blank=True, max_length=100)),
                ('phone', models.CharField(blank=True, max_length=50)),
                ('address', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='contactpage',
            name='page_ptr',
        ),
        migrations.DeleteModel(
            name='ContactPage',
        ),
    ]
