import requests
import os
from dotenv import load_dotenv
import datetime

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

    # ---- ADD THIS BLOCK ----
    print("=" * 50)
    print("SENDING AT:", datetime.datetime.now())
    print("Sending to:", phone)
    print("=" * 50)
    # -------------------------


    response = requests.post(url, headers=headers, json=data)
    print("Status:", response.status_code)
    print("Full Response:", response.text)
    print("Response:", response.json())

    return response.json()


def send_whatsapp_text(phone, text):
    """Send a free-form text reply. Only works within the 24h customer
    service window (i.e. after the customer has messaged you recently)."""
    phone = format_phone(phone)

    url = f"https://graph.facebook.com/v25.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "text",
        "text": {"body": text},
    }

    response = requests.post(url, headers=headers, json=data)
    print("Send text status:", response.status_code, response.text)
    return response.json()


def download_whatsapp_media(media_id):
    """
    WhatsApp media comes through the webhook only as a media_id.
    Step 1: ask Graph API for the real (temporary, ~5 min) download URL.
    Step 2: download the bytes from that URL, still passing the auth header.
    Returns (content_bytes, mime_type) or (None, None) on failure.
    """
    headers = {"Authorization": f"Bearer {TOKEN}"}

    meta_resp = requests.get(f"https://graph.facebook.com/v25.0/{media_id}", headers=headers)
    if meta_resp.status_code != 200:
        print("Media lookup failed:", meta_resp.status_code, meta_resp.text)
        return None, None

    meta = meta_resp.json()
    media_url = meta.get("url")
    mime_type = meta.get("mime_type")

    if not media_url:
        return None, None

    file_resp = requests.get(media_url, headers=headers)
    if file_resp.status_code != 200:
        print("Media download failed:", file_resp.status_code)
        return None, None

    return file_resp.content, mime_type


def send_order_complete_message(order):
    phone = format_phone(order.customer.phone)

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
            "name": "order_completed",
            "language": {"code": "en"},
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {"type": "text", "text": order.customer.name},
                        {"type": "text", "text": order.work_name},
                    ]
                }
            ]
        }
    }

    print("=" * 50)
    print("SENDING ORDER COMPLETE MSG AT:", datetime.datetime.now())
    print("Order:", order.id, "-> Phone:", phone)
    print("=" * 50)

    response = requests.post(url, headers=headers, json=data)
    print("Status:", response.status_code)
    print("Response:", response.text)

    return response.json()