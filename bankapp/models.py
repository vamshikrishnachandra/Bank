from django.db import models
from django.core.validators import RegexValidator

class Bank(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class StatementType(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class AccountDetails(models.Model):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    account_number = models.CharField(
        max_length=50, 
        blank=True,
        null=True, 
        validators=[ 
            RegexValidator(
                regex=r'^\d{10,16}$', 
                message='Account number must be 10-16 digits'
            )
        ]
    )
    account_holder_name = models.CharField(max_length=255, null=True, blank=True)
    statement_start_date = models.DateField(null=True, blank=True)
    statement_end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.bank.name} - {self.account_number}"

class BankStatement(models.Model):
    account_details = models.ForeignKey(AccountDetails, on_delete=models.CASCADE, related_name='transactions',blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    description = models.TextField()
    amount = models.DecimalField(max_digits=15, decimal_places=2,blank=True, null=True)
    type = models.CharField(
        max_length=50, 
        choices=[('CR', 'Credit'), ('DR', 'Debit')],
        default='DR'
    )

    def __str__(self):
        return f'{self.date} - {self.description} - {self.amount} {self.type}'
