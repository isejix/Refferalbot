import requests

payment = "https://api.zarinpal.com/pg/v4/payment/request.json"
merchant_id = "722e8cf9-74d6-411d-bc7f-604160acc74f"

def link_payment(amount: float):
    response = requests.post(payment, json={
        "merchant_id": merchant_id,
        "amount": int(amount), 
        "currency": "IRR",
        "description": "خرید رفرال ربات",
        "callback_url": "https://www.google.com"
    })

    if response.status_code == 200:
        response_data = response.json()
        if response_data.get("data") and response_data["data"].get("code") == 100:
            return f"https://www.zarinpal.com/pg/StartPay/{response_data['data']['authority']}"
        else:
            raise ValueError(f"Payment request failed: {response_data.get('errors', {}).get('message', 'Unknown error')}")
    else:
        raise ConnectionError(f"Failed to connect to payment gateway. Status code: {response.status_code}")



def check_status_payment(amount, x):
    response = requests.post("https://payment.zarinpal.com/pg/v4/payment/verify.json", {
        "merchant_id": merchant_id,
        "amount": int(float(amount)),
        "authority": x
    })
    if response.status_code == 200:
        if 'errors' in response and response['errors']['message'] == 'Session is not valid, session is not active paid try.':
            return "error not active"
        else:
            return response.json()["data"]["code"]
    else:
        raise ConnectionError(f"Failed to connect to payment gateway. Status code: {response.status_code}")
