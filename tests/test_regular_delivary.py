import pytest
from delivery_rule import BasicDeliveryRule
from enums import DeliveryProviderEnum, PackageSizeEnum
from member import Member
from delivery import Delivery
from transaction import Transaction
from datetime import date

LP_S = 1.5
LP_M = 4.9
LP_L = 6.9

MR_S = 2
MR_M = 3
MR_L = 4


@pytest.fixture
def delivery_rules():
    
    
    
    return [
        BasicDeliveryRule(DeliveryProviderEnum.LP, PackageSizeEnum.S, LP_S),
        BasicDeliveryRule(DeliveryProviderEnum.LP, PackageSizeEnum.M, LP_M),
        BasicDeliveryRule(DeliveryProviderEnum.LP, PackageSizeEnum.L, LP_L),
        BasicDeliveryRule(DeliveryProviderEnum.MR, PackageSizeEnum.S, MR_S),
        BasicDeliveryRule(DeliveryProviderEnum.MR, PackageSizeEnum.M, MR_M),
        BasicDeliveryRule(DeliveryProviderEnum.MR, PackageSizeEnum.L, MR_L),
    ]

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