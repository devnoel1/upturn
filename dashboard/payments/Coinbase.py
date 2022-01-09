from coinbase_commerce.client import Client
from coinbase_commerce.webhook import Webhook
from dashboard.payments.update_account import UserAccount

class Coinbase:
    def __init__(self):
        self.api_key = "7f749472-57ca-415e-ae02-f5c3c86928cf"
        self.secret = "d5f88b49-7d76-4486-8013-821787e50a39"
        self.client =  Client(api_key=self.api_key)

    def createCharge(self,amount,user,method=None):
        data =  {
                    "name": "Upturn",
                    "description": "Depositing to account",
                    "local_price": {
                        "amount": amount,
                        "currency": "USD"
                    },
                     "pricing_type": "fixed_price",
                    "metadata": {
                        "customer_id": user.pk,
                        "customer_name": user.first_name + user.last_name
                    },
                        "redirect_url": "http://127.0.0.1:8000/user/coinbase_success",
                        "cancel_url": "http://127.0.0.1:8000/user/coinbase_cancel"
                }
        charge = self.client.charge.create(**data)

        UserAccount.insert_transaction(user,amount,charge['id'],method)

        return charge

    def createCheckout(self,amount,user,method=None):
        checkout = self.client.checkout.create(
                name='The Sovereign Individual',
                description='Mastering the Transition to the Information Age',
                pricing_type='fixed_price',
                local_price={
                "amount": "100.00",
                "currency": "USD"
                },
                requested_info=["name", "email"]
            ) 
    
    def webhooks(self,request_data,request_sig):
        return Webhook.construct_event(request_data, request_sig, self.secret)
             
        
