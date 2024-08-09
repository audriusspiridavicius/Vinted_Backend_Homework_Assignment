import pytest
from transaction import Transaction
from enums import PackageSizeEnum, DeliveryProviderEnum


class TestTransaction:
    
    @pytest.mark.parametrize("date, size, delivery_provider",[("2010-12-10","S","LP"),("2024-12-10","S","MR"),("2024-12-10","L","LP")])
    def test_correct_data(self, date, size, delivery_provider):
        
        transaction = Transaction(date, size, delivery_provider)
        assert isinstance(transaction.package_size, PackageSizeEnum)
        assert isinstance(transaction.provider, DeliveryProviderEnum)  
        assert transaction.ignored == False
    
    @pytest.mark.parametrize("date, size, delivery_provider",[("02010-12-10","S","LP"),("2024g-12-10","S","MR"),
                                                              ("2024-aa-10","L","LP"), ("afdsdsf","L","LP")])
    def test_invalid_date(self, date, size, delivery_provider):
        transaction = Transaction(date, size, delivery_provider)
        assert transaction.ignored == True
    
    @pytest.mark.parametrize("date, size, delivery_provider",[("2010-12-10","","LP"),("2010-12-10","0","LP"),("2024-12-10","SS","MR"),("2024-12-10","!","LP")])
    def test_invalid_package_size(self, date, size, delivery_provider):
        
        transaction = Transaction(date, size, delivery_provider)
        assert transaction.ignored == False
        assert isinstance(transaction.package_size, str) 
    
    @pytest.mark.parametrize("date, size, delivery_provider",[("2010-12-10","S","LP1"),("2024-12-10","S",""),("2024-12-10","L","123456")])
    def test_invalid_delivery_provider(self, date, size, delivery_provider):
        
        transaction = Transaction(date, size, delivery_provider)
        assert transaction.ignored == False
        assert isinstance(transaction.provider, str) 
    