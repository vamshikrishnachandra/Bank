import re
from PyPDF2 import PdfReader
from datetime import datetime

def extract_data_from_pdf(file):
    """
    Extract account details and transactions from a bank statement PDF.
    """

    # Read the PDF
    reader = PdfReader(file)
    text = " ".join(page.extract_text() for page in reader.pages)

    # Define regex patterns for account details
    account_number_pattern = r"Account\s*Number[:\s]*([\d\-]+)"
    account_holder_pattern = r"Account\s*Holder[:\s]*([\w\s]+)"
    bank_name_pattern = r"Bank[:\s]*([\w\s]+)"
    branch_pattern = r"Branch[:\s]*([\w\s]+)"

    # Extract account details
    account_data = {
        "account_number": re.search(account_number_pattern, text).group(1).strip(),
        "account_holder_name": re.search(account_holder_pattern, text).group(1).strip(),
        "bank": re.search(bank_name_pattern, text).group(1).strip(),
        "branch": re.search(branch_pattern, text).group(1).strip() if re.search(branch_pattern, text) else None,
    }

    # Define regex pattern for transactions (Example format: Date, Description, Amount, Balance)
    transaction_pattern = r"(\d{2}/\d{2}/\d{4})\s+([\w\s]+?)\s+([\d,]+\.\d{2})\s+([\d,]+\.\d{2})\s+(Credit|Debit)"

    transactions = []
    for match in re.finditer(transaction_pattern, text):
        txn_date, description, amount, balance, transaction_type = match.groups()

        # Parse the transaction details
        transactions.append({
            "txn_date": datetime.strptime(txn_date, "%d/%m/%Y").date(),
            "description": description.strip(),
            "amount": float(amount.replace(",", "")),
            "balance": float(balance.replace(",", "")),
            "transaction_type": transaction_type.lower(),
        })

    return account_data, transactions
