# Generated by Django 5.1.3 on 2024-11-25 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bankapp', '0008_remove_transaction_additional_info_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transaction',
            options={},
        ),
        migrations.AddField(
            model_name='transaction',
            name='additional_info',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(choices=[('credit', 'Credit'), ('debit', 'Debit')], default=None, max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='cheque_no',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='deposits',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='txn_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='value_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='withdrawals',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=20),
        ),
    ]
