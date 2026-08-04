import pytest
from reference.bank import BankAccount

@pytest.fixture
def zero_bank_account():
    return BankAccount()
    
@pytest.fixture
def bank_account():
    return BankAccount(50)

def test_zero_balance(zero_bank_account):
    assert zero_bank_account.balance == 0

@pytest.mark.parametrize("deposit, current", [(50, 100), (17, 67), (22, 72)])
def test_deposit(bank_account, deposit, current):
    bank_account.deposit(deposit)
    assert bank_account.balance == current
    
@pytest.mark.parametrize("withdraw, current", [(50, 0), (17, 33), (21, 29)])
def test_withdraw(bank_account, withdraw, current):
    bank_account.withdraw(withdraw)
    assert bank_account.balance == current
    
def test_insufficient_funds(bank_account):
    with pytest.raises(Exception):
        bank_account.withdraw(52)