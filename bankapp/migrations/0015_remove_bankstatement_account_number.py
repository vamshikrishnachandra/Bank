# Generated by Django 5.1.3 on 2024-12-03 10:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bankapp', '0014_alter_bankstatement_account_number_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bankstatement',
            name='account_number',
        ),
    ]