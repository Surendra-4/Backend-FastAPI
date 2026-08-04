class InsufficientFunds(Exception):
    pass

class BankAccount:
    
    def __init__(self, initial_amount: int = 0):
        self.balance = initial_amount
        
    def set_balance(self, num: int):
        self.balance = num
    
    def deposit(self, amount: int):
        self.balance += amount
        
    def withdraw(self, amount: int):
        if self.balance < amount:
            raise InsufficientFunds("Insufficient funds")
        self.balance -= amount
        
    def interest(self):
        self.balance * 0.1