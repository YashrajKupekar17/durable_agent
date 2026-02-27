from tools.create_invoice import create_invoice

if __name__ == "__main__":

    args_create = {
        "email": "ziggy.tardigrade@example.com",
        "amount": 150.00,
        "description": "Flight to Replay",
        "days_until_due": 7,
    }
    invoice_details = create_invoice(args_create)
    print(invoice_details)