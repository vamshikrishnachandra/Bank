from datetime import datetime
from decimal import Decimal, InvalidOperation
from PyPDF2 import PdfReader
import fitz
import pdfplumber
import re

def extract_account_number(text):
    # Use regex or other logic to extract the account number
    match = re.search(r'Account Number:\s*(\d+)', text)
    return match.group(1) if match else None

def extract_account_holder_name(text):
    # Use regex or other logic to extract the account holder's name
    match = re.search(r'Account Holder:\s*(\w+\s\w+)', text)
    return match.group(1) if match else None

def extract_statement_dates(text):
    # Logic to extract statement dates
    dates = re.findall(r'(\d{2}/\d{2}/\d{4})', text)
    return dates

def parse_icic_bank_statement(pdf_file):
    parsed_data = {
        'account_number': None,
        'account_holder_name': None,
        'statement_dates': [],
        'transactions': [],
    }

    try:
        if not hasattr(pdf_file, 'read'):
            raise ValueError("The input `pdf_file` should be a file object, not a string or unsupported type.")

        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    # Extract account details
                    if not parsed_data['account_number']:
                        parsed_data['account_number'] = extract_account_number(text)
                    if not parsed_data['account_holder_name']:
                        parsed_data['account_holder_name'] = extract_account_holder_name(text)

                    # Extract statement dates and parse using parse_date
                    statement_dates = extract_statement_dates(text)
                    if statement_dates:
                        # Apply date parsing on each extracted date
                        parsed_data['statement_dates'] = [parse_date(date) for date in statement_dates]

                    # Extract table data (e.g., transactions)
                    table = page.extract_table()
                    if table:
                        header = [col.strip().lower() for col in table[0] if col]
                        if 'txn date' in header and 'withdrawals (dr)' in header and 'deposits (cr)' in header:
                            for row in table[1:]:  # Skip header
                                if len(row) == len(header):  # Ensure row matches header
                                    parsed_data['transactions'].append(parse_icici_row(row, header))
                        else:
                            for row in table[1:]:  # Generic case
                                if len(row) >= 3:  # Ensure the row has the necessary columns
                                    parsed_data['transactions'].append({
                                        'date': parse_date(row[0]),
                                        'description': row[1],
                                        'amount': clean_amount(row[2]),
                                        'type': extract_type(row[3]) if len(row) > 3 else 'Unknown',
                                    })

        return parsed_data

    except Exception as e:
        return {"error": f"Error processing the file: {e}"}

# Helper function for parsing individual rows (ICICI)
def parse_icici_row(row, header):
    transaction = {}
    for i, column in enumerate(row):
        if header[i] == 'txn date':
            transaction['date'] = parse_date(column)
        elif header[i] == 'withdrawals (dr)':
            transaction['withdrawal'] = clean_amount(column)
        elif header[i] == 'deposits (cr)':
            transaction['deposit'] = clean_amount(column)
    return transaction

def parse_date(date_str):
    try:
        # Try both formats: 'DD/MM/YYYY' and 'DD-MM-YYYY'
        for fmt in ('%d/%m/%Y', '%d-%m-%Y'):
            try:
                date_obj = datetime.strptime(date_str, fmt)
                return date_obj.strftime('%Y-%m-%d')  # Convert to 'YYYY-MM-DD' format
            except ValueError:
                continue
        # If both formats fail, return None or raise an exception
        return None
    except Exception as e:
        # Log or handle the exception
        return None


def clean_amount(amount_str):
    # Clean and convert amount to float or integer
    return float(amount_str.replace(',', '').replace('₹', '').strip()) if amount_str else 0.0

def extract_type(transaction_type):
    # Logic to extract transaction type (CR/DR)
    if transaction_type.upper() == 'CR':
        return 'CR'
    elif transaction_type.upper() == 'DR':
        return 'DR'
    return 'None'  # Default case if not CR/DR


def parse_icic_creditcard_statement(pdf_file):
    parsed_data = {
        'account_number': None,
        'card_holder_name': None,
        'statement_dates': [],
        'transactions': [],
    }

    try:
        if not hasattr(pdf_file, 'read'):
            raise ValueError("The input `pdf_file` should be a file object, not a string or unsupported type.")

        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    # Extract account details
                    if not parsed_data['account_number']:
                        parsed_data['account_number'] = extract_account_number(text)
                    if not parsed_data['card_holder_name']:
                        parsed_data['card_holder_name'] = extract_account_holder_name(text)

                    # Extract statement dates
                    statement_dates = extract_statement_dates(text)
                    if statement_dates:
                        parsed_data['statement_dates'].extend(statement_dates)

                    # Extract table data (e.g., transactions)
                    table = page.extract_table()
                    if table:
                        header = [col.strip().lower() for col in table[0] if col]
                        if 'txn date' in header and 'amount' in header:
                            for row in table[1:]:  # Skip header
                                if len(row) == len(header):  # Ensure row matches header
                                    parsed_data['transactions'].append(parse_icici_creditcard_row(row, header))

        return parsed_data

    except Exception as e:
        return {"error": f"Error processing the file: {e}"}

# Helper function for parsing credit card rows (ICICI)
def parse_icici_creditcard_row(row, header):
    transaction = {}
    for i, column in enumerate(row):
        if header[i] == 'txn date':
            transaction['date'] = parse_date(column)
        elif header[i] == 'amount':
            transaction['amount'] = clean_amount(column)
    return transaction

def parse_icic_debitcard_statement(pdf_file):
    parsed_data = {
        'account_number': None,
        'card_holder_name': None,
        'statement_dates': [],
        'transactions': [],
    }

    try:
        if not hasattr(pdf_file, 'read'):
            raise ValueError("The input `pdf_file` should be a file object, not a string or unsupported type.")

        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    # Extract account details
                    if not parsed_data['account_number']:
                        parsed_data['account_number'] = extract_account_number(text)
                    if not parsed_data['card_holder_name']:
                        parsed_data['card_holder_name'] = extract_account_holder_name(text)

                    # Extract statement dates
                    statement_dates = extract_statement_dates(text)
                    if statement_dates:
                        parsed_data['statement_dates'].extend(statement_dates)

                    # Extract table data (e.g., transactions)
                    table = page.extract_table()
                    if table:
                        header = [col.strip().lower() for col in table[0] if col]
                        if 'txn date' in header and 'amount' in header:
                            for row in table[1:]:  # Skip header
                                if len(row) == len(header):  # Ensure row matches header
                                    parsed_data['transactions'].append(parse_icici_debitcard_row(row, header))

        return parsed_data

    except Exception as e:
        return {"error": f"Error processing the file: {e}"}

# Helper function for parsing debit card rows (ICICI)
def parse_icici_debitcard_row(row, header):
    transaction = {}
    for i, column in enumerate(row):
        if header[i] == 'txn date':
            transaction['date'] = parse_date(column)
        elif header[i] == 'amount':
            transaction['amount'] = clean_amount(column)
    return transaction


def parse_idbi_bank_statement(pdf_file):
    """
    Parse IDBI Bank PDF statement and extract account details and transactions.
    :param pdf_file: InMemoryUploadedFile object (the uploaded PDF)
    :return: Parsed data dictionary containing account details and transactions
    """
    parsed_data = {
        'account_number': None,
        'account_holder_name': None,
        'statement_dates': [],
        'transactions': []
    }

    # Open the uploaded PDF file with pdfplumber
    with pdfplumber.open(pdf_file) as pdf:
        full_text = ""
        # Extract the full text from all pages
        for page in pdf.pages:
            full_text += page.extract_text()

     
        # Extract Account Number
        account_match = re.search(r'Account\s+No[:\s]*([\d]+)', full_text)
        if account_match:
            parsed_data['account_number'] = account_match.group(1)

        # Extract Account Holder Name
        # Update regex to match variations in the format of "Account Holder Name"
        account_holder_match = re.search(r'Account\s+Holder\s+Name[:\s]*([a-zA-Z\s]+)', full_text)

        if not account_holder_match:
            # Try matching with alternative phrasing, accounting for possible extra spaces
            account_holder_match = re.search(r'Account\s+Holder\s*[:\s]*([a-zA-Z\s]+)', full_text)

        if account_holder_match:
            parsed_data['account_holder_name'] = account_holder_match.group(1)
  

        # Extract Statement Dates (start and end)
        date_match = re.search(r'Transaction Date From (\d{2}-[A-Za-z]{3}-\d{4}) to (\d{2}-[A-Za-z]{3}-\d{4})', full_text)
        if date_match:
            statement_start_date = datetime.strptime(date_match.group(1), "%d-%b-%Y").date()
            statement_end_date = datetime.strptime(date_match.group(2), "%d-%b-%Y").date()
            parsed_data['statement_dates'] = [statement_start_date, statement_end_date]
       

        # Process Tables for Transactions
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    # Skip invalid or header rows
                    if not row or "Txn Date" in row[0] or "S.No" in row[0]:
                        continue

                    try:
                        # Extract Transaction Data
                        txn_date_str = row[1].strip() if row[1] else ""
                        
                        # Only extract the date part (ignoring time)
                        txn_date = datetime.strptime(txn_date_str.split()[0], "%d/%m/%Y").date() if txn_date_str else None  # Txn Date
                        description = row[3].strip() if row[3] else ""  # Description
                        withdrawals = row[5].replace(",", "").strip() if row[5] else None  # Withdrawals
                        deposits = row[6].replace(",", "").strip() if row[6] else None  # Deposits

                        # Ensure at least one of withdrawals or deposits exists
                        if not withdrawals and not deposits:
                            continue  # Skip rows with missing withdrawal/deposit data

                        # Determine the transaction type (DR or CR)
                        amount = float(withdrawals if withdrawals else deposits)
                        txn_type = "DR" if withdrawals else "CR"

                        # Append the transaction data to the list
                        parsed_data['transactions'].append({
                            'date': txn_date,
                            'description': description,
                            'amount': amount,
                            'type': txn_type
                        })
                    except (ValueError, IndexError) as e:
                        # Skip rows with errors in parsing
                        # print(f"Skipping row due to error: {row}, {e}")
                        continue

    return parsed_data
def parse_idbi_debitcard_statement(pdf_file):
    """
    Parses IDBI Debit Card Statement PDF.
    """
    parsed_data = {
        'account_number': None,
        'account_holder_name': None,
        'statement_dates': [],
        'transactions': []
    }

    try:
        reader = PdfReader(pdf_file)
        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text()

        # Extract Account Number
        account_number_match = re.search(r"Card Number\s*:\s*(\d+)", full_text)
        if account_number_match:
            parsed_data['account_number'] = account_number_match.group(1).strip()

        # Extract Transactions (Debit card-specific format)
        transaction_pattern = re.compile(
            r"(\d{2}-\d{2}-\d{4})\s+"      # Transaction Date
            r"(.+?)\s+"                    # Description
            r"([\d,]+\.\d{2})\s+"          # Transaction Amount
            r"(\w+)"                       # Type (DR/CR)
        )

        for match in transaction_pattern.finditer(full_text):
            txn_date = datetime.strptime(match.group(1), "%d-%m-%Y").date()
            description = match.group(2).strip()
            amount = float(match.group(3).replace(',', ''))
            txn_type = match.group(4)

            parsed_data['transactions'].append({
                'date': txn_date,
                'description': description,
                'amount': amount,
                'type': txn_type
            })

        return parsed_data

    except Exception as e:
        return {'error': str(e)}

def parse_idbi_creditcard_statement(pdf_file):
    """
    Parses IDBI Credit Card Statement PDF.
    """
    parsed_data = {
        'account_number': None,
        'account_holder_name': None,
        'statement_dates': [],
        'transactions': []
    }

    try:
        reader = PdfReader(pdf_file)
        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text()

        # Extract Card Number
        card_number_match = re.search(r"Card Number\s*:\s*(\d+)", full_text)
        if card_number_match:
            parsed_data['account_number'] = card_number_match.group(1).strip()

        # Extract Transactions (Credit card-specific format)
        transaction_pattern = re.compile(
            r"(\d{2}-\d{2}-\d{4})\s+"      # Transaction Date
            r"(.+?)\s+"                    # Description
            r"([\d,]+\.\d{2})\s+"          # Transaction Amount
            r"(\w+)"                       # Type (DR/CR)
        )

        for match in transaction_pattern.finditer(full_text):
            txn_date = datetime.strptime(match.group(1), "%d-%m-%Y").date()
            description = match.group(2).strip()
            amount = float(match.group(3).replace(',', ''))
            txn_type = match.group(4)

            parsed_data['transactions'].append({
                'date': txn_date,
                'description': description,
                'amount': amount,
                'type': txn_type
            })

        return parsed_data

    except Exception as e:
        return {'error': str(e)}
    
    
def parse_date(date_str):
    """Parses a date string to a datetime object."""
    try:
        return datetime.strptime(date_str, "%d/%m/%Y").date()
    except:
        return None

def convert_to_decimal(amount_str):
    try:
        # Ensure the string is valid and clean
        if not amount_str or amount_str.strip() == "":
            return Decimal("0.00")
        
        # Remove commas, strip whitespace, and attempt conversion
        return Decimal(amount_str.replace(",", "").strip())
    except (InvalidOperation, ValueError, AttributeError):
        return Decimal("0.00")


# Parse HDFC Bank Statement Function
# Helper Function: Parse date strings
def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%d/%m/%Y").date()
    except (ValueError, TypeError):
        return None
# Main Function: Parse HDFC Bank Statement PDF
def parse_hdfc_bank_statement(uploaded_pdf):
    parsed_data = {
        'account_number': None,
        'statement_dates': [],
        'transactions': []
    }

    with pdfplumber.open(uploaded_pdf) as pdf:
        for page_num, page in enumerate(pdf.pages):
            text = page.extract_text()

            # Debugging: Print extracted text
            print(f"Extracted text from page {page_num + 1}:")
            print(text)

            # Extract account details (debugged)
            account_number_match = re.search(r'Account No[:\s]+(\d+)', text)
            if account_number_match and not parsed_data['account_number']:
                parsed_data['account_number'] = account_number_match.group(1)
                print(f"Account Number Found: {parsed_data['account_number']}")

            # Extract statement dates (debugged)
            date_match = re.search(r'Statement From\s*:\s*(\d{2}/\d{2}/\d{4})\s*To\s*:\s*(\d{2}/\d{2}/\d{4})', text)
            if date_match and not parsed_data['statement_dates']:
                parsed_data['statement_dates'] = [
                    parse_date(date_match.group(1)),
                    parse_date(date_match.group(2))
                ]
                print(f"Statement Dates Found: {parsed_data['statement_dates']}")

            # Extract Transactions Table
            transactions_table = page.extract_tables()
            if transactions_table:
                for table in transactions_table:
                    for row in table:
                        if len(row) >= 6:
                            date_str = row[0].strip() if row[0] else None
                            description = row[1].strip() if row[1] else ""
                            withdrawal_str = row[4].strip() if row[4] else '0.00'
                            deposit_str = row[5].strip() if row[5] else '0.00'

                            date = parse_date(date_str)
                            withdrawal_amount = convert_to_decimal(withdrawal_str)
                            deposit_amount = convert_to_decimal(deposit_str)

                            if withdrawal_amount > Decimal("0.00"):
                                transaction_type = "Debit"
                                amount = withdrawal_amount
                            elif deposit_amount > Decimal("0.00"):
                                transaction_type = "Credit"
                                amount = deposit_amount
                            else:
                                continue

                            if date:
                                parsed_data['transactions'].append({
                                    'date': date,
                                    'description': description,
                                    'amount': amount,
                                    'type': transaction_type
                                })
    
    # Final validation
    if not parsed_data['account_number']:
        raise ValueError("Account number not found in the statement.")
    if not parsed_data['statement_dates']:
        raise ValueError("Statement dates not found in the statement.")
    if not parsed_data['transactions']:
        raise ValueError("No transactions found in the statement.")
    
    return parsed_data

# Function to parse HDFC Debitcard Statement
def parse_hdfc_debitcard_statement(uploaded_pdf):
    parsed_data = {
        'account_number': None,
        'account_holder_name': None,
        'statement_dates': [],
        'transactions': []
    }

    with pdfplumber.open(uploaded_pdf) as pdf:
        first_page = pdf.pages[0]
        text = first_page.extract_text()

        # Extract account number and holder name
        account_number_match = re.search(r'Account No[:\s]+(\d+)', text)
        account_holder_match = re.search(r'Account Holder[:\s]+(.+)', text)
        
        if account_number_match:
            parsed_data['account_number'] = account_number_match.group(1)
        if account_holder_match:
            parsed_data['account_holder_name'] = account_holder_match.group(1)

        # Extract statement dates
        date_match = re.search(r'Statement From\s*:\s*(\d{2}/\d{2}/\d{4})\s*To\s*:\s*(\d{2}/\d{2}/\d{4})', text)
        if date_match:
            parsed_data['statement_dates'] = [
                parse_date(date_match.group(1)), 
                parse_date(date_match.group(2))
            ]

        # Extract transactions
        transactions_table = first_page.extract_tables()
        if transactions_table:
            for row in transactions_table[0]:
                # Each row is in the format: [Date, Description, Chq./Ref.No., Value Dt., Withdrawal Amt., Deposit Amt., Closing Balance]
                date = parse_date(row[0])
                description = row[1]
                withdrawal_amount = convert_to_decimal(row[4] if row[4] else '0.00')

                deposit_amount = row[5] if row[5] else '0.00'
                
                # Determine the type of transaction
                if withdrawal_amount > Decimal('0.00'):
                    transaction_type = 'Debit'
                    amount = withdrawal_amount
                elif deposit_amount > Decimal('0.00'):
                    transaction_type = 'Credit'
                    amount = deposit_amount
                else:
                    continue

                # Append to transactions list
                parsed_data['transactions'].append({
                    'date': date,
                    'description': description,
                    'amount': amount,
                    'type': transaction_type
                })

    return parsed_data

# Function to parse HDFC Creditcard Statement
def parse_hdfc_creditcard_statement(uploaded_pdf):
    parsed_data = {
        'account_number': None,
        'account_holder_name': None,
        'statement_dates': [],
        'transactions': []
    }

    with pdfplumber.open(uploaded_pdf) as pdf:
        first_page = pdf.pages[0]
        text = first_page.extract_text()

        # Extract account number and holder name
        account_number_match = re.search(r'Account No[:\s]+(\d+)', text)
        account_holder_match = re.search(r'Account Holder[:\s]+(.+)', text)
        
        if account_number_match:
            parsed_data['account_number'] = account_number_match.group(1)
        if account_holder_match:
            parsed_data['account_holder_name'] = account_holder_match.group(1)

        # Extract statement dates
        date_match = re.search(r'Statement From\s*:\s*(\d{2}/\d{2}/\d{4})\s*To\s*:\s*(\d{2}/\d{2}/\d{4})', text)
        if date_match:
            parsed_data['statement_dates'] = [
                parse_date(date_match.group(1)), 
                parse_date(date_match.group(2))
            ]

        # Extract transactions
        transactions_table = first_page.extract_tables()
        if transactions_table:
            for row in transactions_table[0]:
                # Each row is in the format: [Date, Description, Chq./Ref.No., Value Dt., Withdrawal Amt., Deposit Amt., Closing Balance]
                date = parse_date(row[0])
                description = row[1]
                withdrawal_amount = convert_to_decimal(row[4] if row[4] else '0.00')

                deposit_amount = row[5] if row[5] else '0.00'
                
                # Determine the type of transaction
                if withdrawal_amount > Decimal('0.00'):
                    transaction_type = 'Debit'
                    amount = withdrawal_amount
                elif deposit_amount > Decimal('0.00'):
                    transaction_type = 'Credit'
                    amount = deposit_amount
                else:
                    continue

                # Append to transactions list
                parsed_data['transactions'].append({
                    'date': date,
                    'description': description,
                    'amount': amount,
                    'type': transaction_type
                })

    return parsed_data
