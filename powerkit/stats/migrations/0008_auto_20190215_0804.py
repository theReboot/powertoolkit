# Generated by Django 2.1.5 on 2019-02-15 08:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0007_statspage_performance'),
    ]

    operations = [
        migrations.CreateModel(
            name='RemittanceDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disco', models.CharField(max_length=50)),
                ('invoice_value', models.DecimalField(decimal_places=2, max_digits=15)),
                ('disco_payment', models.DecimalField(decimal_places=2, max_digits=15)),
                ('performance_ratio', models.DecimalField(decimal_places=2, max_digits=5)),
                ('loss', models.DecimalField(decimal_places=2, max_digits=15)),
                ('inefficiency_ratio', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='RemittanceSummary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.IntegerField(choices=[(0, 'Jan'), (1, 'Feb'), (2, 'Mar'), (3, 'Apr'), (4, 'May'), (5, 'Jun'), (6, 'Jul'), (7, 'Aug'), (8, 'Sep'), (9, 'Oct'), (10, 'Nov'), (11, 'Dec')])),
                ('year', models.IntegerField()),
                ('csv_file', models.FileField(upload_to='')),
            ],
            options={
                'verbose_name_plural': 'Remittance Summary',
            },
        ),
        migrations.AddField(
            model_name='remittancedetail',
            name='summary',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stats.RemittanceSummary'),
        ),
        migrations.AddField(
            model_name='statspage',
            name='remittance',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='stats.RemittanceSummary'),
        ),
    ]
