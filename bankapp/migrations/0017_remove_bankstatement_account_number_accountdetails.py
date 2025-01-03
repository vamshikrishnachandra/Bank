# Generated by Django 5.1.3 on 2024-12-09 06:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bankapp', '0016_bankstatement_account_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bankstatement',
            name='account_number',
        ),
        migrations.CreateModel(
            name='AccountDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_number', models.CharField(blank=True, max_length=20, null=True)),
                ('statement_start_date', models.DateField(blank=True, null=True)),
                ('statement_end_date', models.DateField(blank=True, null=True)),
                ('bank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bankapp.bank')),
            ],
        ),
    ]
