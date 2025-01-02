from decimal import Decimal
from django.http import JsonResponse
from django.shortcuts import render
from .models import AccountDetails, Bank, StatementType, BankStatement
from .serializers import BankSerializer, StatementTypeSerializer
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt
from bankapp.pdf_parser import parse_hdfc_bank_statement, parse_hdfc_creditcard_statement, parse_hdfc_debitcard_statement, parse_icic_bank_statement, parse_icic_creditcard_statement, parse_icic_debitcard_statement, parse_idbi_bank_statement, parse_idbi_creditcard_statement, parse_idbi_debitcard_statement


# API ViewSets
class BankViewSet(viewsets.ModelViewSet):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer


class StatementTypeViewSet(viewsets.ModelViewSet):
    queryset = StatementType.objects.all()
    serializer_class = StatementTypeSerializer


@csrf_exempt
def upload_pdf(request):
   if request.method == 'POST' and request.FILES.get('file'):
      uploaded_pdf = request.FILES['file']
      bank_name = request.POST.get('bank_name')
      statement_type = request.POST.get('statement_type')

      # Initialize parsed_data
      parsed_data = {}

      # Parse the PDF based on bank and statement type
      if bank_name == "ICICI":
         if statement_type == "Bank Statement":
            parsed_data = parse_icic_bank_statement(uploaded_pdf)
         elif statement_type == "DebitcardStatement":
            parsed_data = parse_icic_debitcard_statement(uploaded_pdf)
         elif statement_type == "CreditcardStatement":
            parsed_data = parse_icic_creditcard_statement(uploaded_pdf)

        # Add other banks as needed, for example, IDBI...
      if bank_name == "IDBI":
         if statement_type == "Bank Statement":
            parsed_data = parse_idbi_bank_statement(uploaded_pdf)
         elif statement_type == "DebitcardStatement":
            parsed_data = parse_idbi_debitcard_statement(uploaded_pdf)
         elif statement_type == "CreditcardStatement":
            parsed_data = parse_idbi_creditcard_statement(uploaded_pdf)
            
      if bank_name == "HDFC":
         print("Vamshi")
         if statement_type == "Bank Statement":
            parsed_data = parse_hdfc_bank_statement(uploaded_pdf)
         elif statement_type == "DebitcardStatement":
            parsed_data = parse_hdfc_debitcard_statement(uploaded_pdf)
         elif statement_type == "CreditcardStatement":
            parsed_data = parse_hdfc_creditcard_statement(uploaded_pdf)
        # Handle the case where parsed data is None or incomplete
      if not parsed_data or 'error' in parsed_data:
         return JsonResponse({'error': 'Error parsing the file or missing data'}, status=400)

      # Check that parsed_data contains the required fields
      if not all(key in parsed_data for key in ['account_number', 'account_holder_name', 'statement_dates', 'transactions']):
         return JsonResponse({'error': 'Missing required parsed data fields'}, status=400)

      # Handle the case where the bank is not found
      try:
         bank = Bank.objects.get(name=bank_name)
      except Bank.DoesNotExist:
         return JsonResponse({'error': 'Bank not found'}, status=400)

      # Save Account Details
       # Extract statement dates safely
      statement_dates = parsed_data.get('statement_dates', [])
      statement_start_date = statement_dates[0] if statement_dates else None
      statement_end_date = statement_dates[-1] if statement_dates else None

      # Save Account Details
      account_details = AccountDetails.objects.create(
         bank=bank,
         account_number=parsed_data['account_number'],
         account_holder_name=parsed_data['account_holder_name'],
         statement_start_date=statement_start_date,
         statement_end_date=statement_end_date,
      )
      # Save Bank Statement Transactions
      for txn in parsed_data['transactions']:
         try:
               BankStatement.objects.create(
                  account_details=account_details,
                  date=txn['date'],
                  description=txn['description'],
                  amount=txn['amount'],
                  type=txn['type']
               )
         except KeyError as e:
               return JsonResponse({'error': f'Missing transaction field: {str(e)}'}, status=400)

      # Return parsed data as a JSON response or render a template
      return JsonResponse({'status': 'success', 'parsed_data': parsed_data})

   return render(request, 'statements/index.html')
   


def statement_pdf(request):
    return render(request, 'statements/index.html')

