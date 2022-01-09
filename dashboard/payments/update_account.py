from dashboard.models import Account, PaymentMethod, Transactions


class UserAccount:
    def update_users_account(user, amount):

        user_infor = Account.objects.get(user=user)

        balance = user_infor.balance

        update_amount = round(float(balance) + float(amount), 2)

        Account.objects.filter(user=user).update(balance = update_amount)

    def insert_transaction(user, amount, ref, method):
        payment_method = PaymentMethod.objects.get(slug=method)
        transaction = Transactions(user=user,amount=amount,trans_ref=ref,method=payment_method, trans_type='deposite')
        transaction.save()

    def update_transaction(ref,status):
        Transactions.objects.filter(trans_ref=ref).update(status=status)
