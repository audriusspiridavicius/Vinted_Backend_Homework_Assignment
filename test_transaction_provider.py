import os
import pytest
import tempfile
from transaction_provider import TransactionProvider, TransactionsFromTextFile, Transaction

@pytest.fixture
def create_test_transaction_file():
    def _create_test_transaction_file(transactions: list[Transaction]) -> str:
        with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.txt') as f:
            for transaction in transactions:
                f.write(f"{transaction}\n")  # Ensure Transaction objects are converted to string properly
            temp_file_name = f.name

        yield temp_file_name

        os.remove(temp_file_name)
    
    return _create_test_transaction_file

@pytest.fixture
def single_transaction(create_test_transaction_file):
    
    # return create_test_transaction_file([Transaction("2012-10-11", "L", "AB")])
    return next(create_test_transaction_file([Transaction("2012-10-11", "L", "AB")]))
    
@pytest.fixture    
def multiple_transactions(create_test_transaction_file):
    
    transactions = []
    for number in range(1,11):
        transactions.append(Transaction(f"2012-10-{number}", f"L{number}", "AB{number}"))
        
    return next(create_test_transaction_file(transactions))

@pytest.fixture
def empty_transaction_file(create_test_transaction_file):
    return next(create_test_transaction_file([]))

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