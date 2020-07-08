import time
from tkinter import messagebox


def decorator_date(func):
    date = time.strftime("%x")

    def wrapper(*args, **kwargs):
        print(str(func.__name__) + "Transaction date: " + str(date))
        return func(*args, **kwargs)

    return wrapper


class Bank(object):
    def __init__(self, bank_name):
        self.customers = []
        self.bank_name = bank_name

    def add_customer(self, account):
        for i in self.customers:
            if i == account:
                return False
        self.customers.append(account)
        return True

    def remove_customer(self, customer):
        return self.customers.remove(customer)

    def balance_generator(self):
        for i in self.customers:
            yield i.balance

    def __repr__(self):
        string = "Bank Customers:\n"
        for i in self.customers:
            string += str(i) + "\n"
        return string


class Account(object):
    def __init__(self, customer_name, account_number, balance, credit_limit):
        self.customer_name = customer_name
        self.account_number = account_number
        self.balance = balance
        self.credit_limit = credit_limit

    @decorator_date
    def withdraw(self, withdraw_amount):
        if withdraw_amount <= self.credit_limit:
            if self.balance - withdraw_amount < 0:
                messagebox.showinfo("Operation failed","Cannot afford this amount of withdraw lack of money")
                return False
            else:
                self.balance -= withdraw_amount
            return True
        messagebox.showinfo("Operation failed", "You have passed the credit limit")
        return False

    @decorator_date
    def deposit(self, deposit_amount):
        self.balance += deposit_amount

    @decorator_date
    def deposit_to_account(self, other, deposit):
        if self.withdraw(deposit):
            other.balance += deposit
            return True
        return False

    def get_balance(self):
        return self.balance

    def __repr__(self):
        return f"[Account: {self.account_number}, Name: {self.customer_name}," \
            f" Balance: {self.balance}, Credit: {self.credit_limit}]"

    def __str__(self):
        return f"[Account: {self.account_number}, Name: {self.customer_name}, " \
            f"Balance: {self.balance}, Credit: {self.credit_limit}]"

    def __eq__(self, other):
        return self.account_number == other.account_number

    def __hash__(self):
        return hash((self.account_number, self.customer_name))


if __name__ == "__main__":
    bank = Bank("Leumi")
    a1 = Account("Jane dow", 1, 15_000, 10_000)
    a2 = Account("Piter parker", 2, 30_000, 12_000)
    a3 = Account("Moran lit", 3, 150_000, 8_000)
    a4 = Account("Moran lit", 3, 150_000, 8_000)

    bank.add_customer(a1)
    bank.add_customer(a2)
    bank.add_customer(a3)

    bank.add_customer(a4)

    bank.balance_generator()

    for i in bank.customers:
        print(i)