import pytest
from reference.calculations import add, subtract, multiply, divide

@pytest.mark.parametrize("num1, num2, result", [(1, 2, 3), (17, 21, 38), (22, 31, 53)])
def test_add(num1, num2, result):
    assert add(num1, num2) == result
    
@pytest.mark.parametrize("num1, num2, result", [(3, 2, 1), (17, 2, 15), (22, 3, 19)])
def test_subtract(num1, num2, result):
    assert subtract(num1, num2) == result

@pytest.mark.parametrize("num1, num2, result", [(1, 2, 2), (17, 2, 34), (22, 3, 66)])   
def test_multiply(num1, num2, result):
    assert multiply(num1, num2) == result

@pytest.mark.parametrize("num1, num2, result", [(2, 1, 2), (16, 2, 8), (22, 11, 2)]) 
def test_divide(num1, num2, result):
    assert divide(num1, num2) == result