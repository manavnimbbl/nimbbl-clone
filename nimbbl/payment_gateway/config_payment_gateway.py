import requests
import random


payment_gateway={
"razorpay":{
"key_id":"Merchant_key_id",
"key_secret":"Merchant_key_secret",
"base_url":"https://api.razorpay.com/v1/",
"health_check":"https://api.razorpay.com/v1/health"},

"payu":{
"key_id":"Merchant_key_id",
"key_secret":"Merchant_key_secret",
"base_url":"https://secure.payu.in/",
"health_check":"https://secure.payu.in/v1/health"}
}

def check_payment_gateway_health(url):
    try:
        response=requests.get(url)
        return response.status_code==200
    except requests.RequestException:
        return False
    
def select_payment_gateway():
    razorpay_health=check_payment_gateway_health(payment_gateway['razorpay']['health_check'])
    payu_health=check_payment_gateway_health(payment_gateway['payu']['health_check'])

    if razorpay_health and payu_health:
        return random.choice(['razorpay','payu'])
    elif razorpay_health:
        return 'razorpay'
    elif payu_health:
        return 'payu'
    else:
        return None
    