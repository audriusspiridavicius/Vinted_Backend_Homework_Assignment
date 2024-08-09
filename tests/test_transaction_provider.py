import datetime
import os
import pytest
import tempfile
from transaction_provider import TransactionProvider, TransactionsFromTextFile, Transaction
from enums import DeliveryProviderEnum, PackageSizeEnum

test_invalid_date_value = "2012a-10-11"
test_invalid_package_size_value = "LL"
test_invalid_delivery_provider_value = "LP123"


@pytest.fixture
def create_test_transaction_file():
    def _create_test_transaction_file(transactions: list[Transaction]) -> str:
        with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.txt') as f:
            for transaction in transactions:
                f.write(f"{transaction}\n")
            temp_file_name = f.name

        yield temp_file_name

        os.remove(temp_file_name)
    
    return _create_test_transaction_file

@pytest.fixture
def single_transaction(create_test_transaction_file):
    
    return next(create_test_transaction_file([Transaction("2012-10-11", PackageSizeEnum.L, DeliveryProviderEnum.LP)]))
    
@pytest.fixture    
def multiple_transactions(create_test_transaction_file):
    
    transactions = []
    for number in range(1,11):
        transactions.append(Transaction(f"2012-10-{number:0>2}", PackageSizeEnum.M, DeliveryProviderEnum.MR))
        
    return next(create_test_transaction_file(transactions))

@pytest.fixture
def empty_transaction_file(create_test_transaction_file):
    return next(create_test_transaction_file([]))


@pytest.fixture
def invalid_date_transaction_file(create_test_transaction_file):
    
    return next(create_test_transaction_file([Transaction(test_invalid_date_value, PackageSizeEnum.L, DeliveryProviderEnum.LP)]))
    
@pytest.fixture
def invalid_package_size_transaction_file(create_test_transaction_file):
    
    return next(create_test_transaction_file([Transaction("2012-10-11", test_invalid_package_size_value, DeliveryProviderEnum.LP)]))

@pytest.fixture
def invalid_delivery_provider_transaction_file(create_test_transaction_file):
    
    return next(create_test_transaction_file([Transaction("2012-10-11", PackageSizeEnum.L, test_invalid_delivery_provider_value)]))

class TestTransactionProvider:
    
    def test_get_transaction(self):
        
        provider = TransactionProvider()
        
        with pytest.raises(NotImplementedError):
            provider.get_transactions()


            
class TestTransactionsFromTextFile:
    
    def test_single_transaction_file(self, single_transaction):
        
        transactions_provider = TransactionsFromTextFile()
        
        transactions = transactions_provider.get_transactions(single_transaction)
        
        assert len(transactions) == 1
    
    def test_get_multiple_transactions_from_file(self, multiple_transactions):
        
        transactions_provider = TransactionsFromTextFile()
        
        transactions = transactions_provider.get_transactions(multiple_transactions)
        
        assert len(transactions) == 10
        
    def test_empty_file(self, empty_transaction_file):
        
        transactions_provider = TransactionsFromTextFile()
        
        transactions = transactions_provider.get_transactions(empty_transaction_file)
        
        assert len(transactions) == 0
        
    def test_date_type(self, single_transaction):
        
        transactions_provider = TransactionsFromTextFile()
        
        transactions = transactions_provider.get_transactions(single_transaction)
        
        assert len(transactions) == 1
        
        transaction = transactions[0]
        
        assert isinstance(transaction.date, datetime.date)
        
    def test_date_not_string_type(self, single_transaction):
        
        transactions_provider = TransactionsFromTextFile()
        
        transactions = transactions_provider.get_transactions(single_transaction)
        
        assert len(transactions) == 1
        
        transaction = transactions[0]
        
        assert not isinstance(transaction.date, str)
        
    def test_date_invalid(self, invalid_date_transaction_file):
        
        transactions_provider = TransactionsFromTextFile()
        transactions = transactions_provider.get_transactions(invalid_date_transaction_file)
        
        assert transactions[0].ignored == True
        assert transactions[0].date == test_invalid_date_value
    
    def test_package_size_invalid_value(self, invalid_package_size_transaction_file):
        transactions_provider = TransactionsFromTextFile()
        transactions = transactions_provider.get_transactions(invalid_package_size_transaction_file)
        
        assert transactions[0].ignored == False
        assert transactions[0].package_size == test_invalid_package_size_value
    
    
    def test_delivery_provider_invalid_value(self, invalid_delivery_provider_transaction_file):
        transactions_provider = TransactionsFromTextFile()
        transactions = transactions_provider.get_transactions(invalid_delivery_provider_transaction_file)
        
        assert transactions[0].ignored == False
        assert transactions[0].provider == test_invalid_delivery_provider_value
    