from pypaystack import Transaction, Customer, Plan
import json
import random
import string

from dashboard.payments.update_account import UserAccount

class PayStack:
    def __init__(self):
        self.authorization_key = "sk_test_a71e02e4742f837349225104f7dc5f5620a08430"

    def make_transaction(self, amount, user, method=None):
        transaction = Transaction(authorization_key=self.authorization_key)
        ref = self.generate_ref(10)
        paystack = transaction.initialize(user.email, amount,reference=ref)
        UserAccount.insert_transaction(user,amount,ref,method)

        return  paystack[3]['authorization_url']

    def verify_payment(self, ref):
        transaction = Transaction(authorization_key=self.authorization_key)

        response  = transaction.verify(ref) 

        return response

    def generate_ref(self,length):  
        sample_string = 'pqrstuvwxy' # define the specific string  
        # define the condition for random string  
        result = ''.join((random.choice(sample_string)) for x in range(length))  
        return result
