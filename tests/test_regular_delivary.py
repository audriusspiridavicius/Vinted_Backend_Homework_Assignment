import pytest
from enums import DeliveryProviderEnum, PackageSizeEnum
from member import Member
from delivery import Delivery
from transaction import Transaction
from datetime import date
from .test_settings import delivery_rules, LP_S, MR_L, MR_M, MR_S, LP_M, LP_L

@pytest.fixture
def delivery(delivery_rules):
    return Delivery(delivery_rules)



class TestRegularDeliveryCalculation:
    
    customer = Member()
   
    def test_small_lp_price(self, delivery:Delivery):
        
        transaction = Transaction(date=date(year=2020, month=10, day=25), package_size=PackageSizeEnum.S, provider=DeliveryProviderEnum.LP)
        delivary_data = delivery.calculate(transaction, self.customer)
        
        assert delivary_data.delivery_price == LP_S
        
    def test_small_mr_price(self, delivery:Delivery):
        
        transaction = Transaction(date=date(year=2020, month=10, day=25), package_size=PackageSizeEnum.S, provider=DeliveryProviderEnum.MR)
        delivary_data = delivery.calculate(transaction, self.customer)
        
        assert delivary_data.delivery_price == MR_S
        
    def test_medium_lp_price(self, delivery:Delivery):
        
        transaction = Transaction(date=date(year=2020, month=10, day=25), package_size=PackageSizeEnum.M, provider=DeliveryProviderEnum.LP)
        delivary_data = delivery.calculate(transaction, self.customer)
        
        assert delivary_data.delivery_price == LP_M
        
    def test_medium_mr_price(self, delivery:Delivery):
        
        transaction = Transaction(date=date(year=2020, month=10, day=25), package_size=PackageSizeEnum.M, provider=DeliveryProviderEnum.MR)
        delivary_data = delivery.calculate(transaction, self.customer)
        
        assert delivary_data.delivery_price == MR_M
        
    def test_large_lp_price(self, delivery:Delivery):
        
        transaction = Transaction(date=date(year=2020, month=10, day=25), package_size=PackageSizeEnum.L, provider=DeliveryProviderEnum.LP)
        delivary_data = delivery.calculate(transaction, self.customer)
        
        assert delivary_data.delivery_price == LP_L
        
    def test_large_mr_price(self, delivery:Delivery):
        
        transaction = Transaction(date=date(year=2020, month=10, day=25), package_size=PackageSizeEnum.L, provider=DeliveryProviderEnum.MR)
        delivary_data = delivery.calculate(transaction, self.customer)
        
        assert delivary_data.delivery_price == MR_L
        
    def test_invalid_package_size(self, delivery:Delivery):
        
        transaction = Transaction(date=date(year=2020, month=10, day=25), package_size="G", provider=DeliveryProviderEnum.MR)
        delivary_data = delivery.calculate(transaction, self.customer)
        
        assert delivary_data.delivery_price == "Ignored"
        
    def test_invalid_delivery_provider(self, delivery:Delivery):
        
        transaction = Transaction(date=date(year=2020, month=10, day=25), package_size=PackageSizeEnum.S, provider="abc")
        delivary_data = delivery.calculate(transaction, self.customer)

        assert delivary_data.delivery_price == "Ignored"
        