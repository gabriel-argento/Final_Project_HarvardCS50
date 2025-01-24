from datetime import datetime
from project import is_valid_stock_code
from project import is_valid_date
from project import is_valid_money
import pytest

# Tests for is_valid_stock_code
def test_is_valid_stock_code_valid():
    assert is_valid_stock_code("AAPL") is True  # Apple stock code should be valid

def test_is_valid_stock_code_invalid():
    assert is_valid_stock_code("INVALIDCODE") is False  # Non-existent stock code should be invalid


# Tests for is_valid_date
def test_is_valid_date_valid():
    assert is_valid_date("2020-01-01 to 2020-12-31") is True  # Valid date range should return True

def test_is_valid_date_invalid_format():
    assert is_valid_date("01/01/2020 to 31/12/2020") is False  # Invalid format should return False

def test_is_valid_date_start_after_end():
    assert is_valid_date("2021-01-01 to 2020-12-31") is False  # Start date after end date should return False

def test_is_valid_date_future_date():
    future_date = (datetime.now().year + 1)
    assert is_valid_date(f"2020-01-01 to {future_date}-12-31") is False  # Date in the future should return False


# Tests for is_valid_money
def test_is_valid_money_valid():
    assert is_valid_money("100") is True  # Positive money value should return True

def test_is_valid_money_zero():
    assert is_valid_money("0") is False  # Zero value should return False

def test_is_valid_money_negative():
    assert is_valid_money("-50") is False  # Negative value should return False

def test_is_valid_money_non_integer():
    assert is_valid_money("abc") is False  # Non-integer value should return False
