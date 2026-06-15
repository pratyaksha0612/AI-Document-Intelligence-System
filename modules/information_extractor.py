import re


def extract_information(text):

    data = {}

    email = re.search(
        r'[\w\.-]+@[\w\.-]+\.\w+',
        text
    )

    phone = re.findall(
    r'\d{10}',
    text
    )
    phone = phone[0] if phone else None

    date = re.search(
        r'\d{2}[-/]\d{2}[-/]\d{4}',
        text
    )

    amount_line = re.search(
        r'Amount[:\s]*(.*)',
        text,
        re.IGNORECASE
    )

    amount = None

    if amount_line:
        amount_text = amount_line.group(1)

        amount = re.search(
            r'[\d,]+',
            amount_text
        )

    data["Email"] = email.group() if email else "Not Found"
    data["Phone"] = phone if phone else "Not Found"
    data["Date"] = date.group() if date else "Not Found"
    
    if amount:
        data["Amount"] = amount.group()
    else:
        data["Amount"] = "Not Found"
    

    return data