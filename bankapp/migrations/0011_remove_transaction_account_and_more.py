# Generated by Django 5.1.3 on 2024-11-30 12:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bankapp', '0010_bank_statementtype_bankstatement'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='account',
        ),
        migrations.RemoveField(
            model_name='bankstatement',
            name='cheque_no',
        ),
        migrations.RemoveField(
            model_name='bankstatement',
            name='deposit',
        ),
        migrations.RemoveField(
            model_name='bankstatement',
            name='narration',
        ),
        migrations.RemoveField(
            model_name='bankstatement',
            name='withdrawal',
        ),
        migrations.AddField(
            model_name='bankstatement',
            name='amount',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='bankstatement',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='bankstatement',
            name='type',
            field=models.CharField(blank=True, choices=[('credit', 'Credit'), ('debit', 'Debit')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='bankstatement',
            name='balance',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='bankstatement',
            name='bank',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bankapp.bank'),
        ),
        migrations.AlterField(
            model_name='bankstatement',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bankstatement',
            name='statement_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bankapp.statementtype'),
        ),
        migrations.DeleteModel(
            name='AccountInfo',
        ),
        migrations.DeleteModel(
            name='Transaction',
        ),
    ]
