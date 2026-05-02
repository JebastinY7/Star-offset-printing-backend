import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

def format_phone(phone):
    phone = ''.join(filter(str.isdigit, str(phone)))

    if phone.startswith("91"):
        return phone

    return f"91{phone}"

def send_whatsapp_template(phone, customer_name, offer_message, shop_number):
    phone = format_phone(phone)

    url = f"https://graph.facebook.com/v25.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "template",
        "template": {
            "name": "special_discount_offer",
            "language": {"code": "en"},
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {"type": "text", "text": customer_name},
                        {"type": "text", "text": offer_message},
                        {"type": "text", "text": shop_number}
                    ]
                }
            ]
        }
    }

    response = requests.post(url, headers=headers, json=data)
    print("Status:", response.status_code)
    print("Full Response:", response.text)
    print("Response:", response.json())

    return response.json()