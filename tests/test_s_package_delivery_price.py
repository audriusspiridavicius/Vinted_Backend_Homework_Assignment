import pytest
from delivery_rule import BasicDeliveryRule
from enums import DeliveryProviderEnum, PackageSizeEnum
from delivery import SmallestDeliveryPriceAmongProviders
from member import Member
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
    return SmallestDeliveryPriceAmongProviders(delivery_rules)

@pytest.fixture
def transaction():
    return Transaction(date=date(year=2020, month=10, day=25), package_size=PackageSizeEnum.S, provider=DeliveryProviderEnum.MR)


class TestSmallPackageDeliveryPrice:
    
    
    customer = Member()
    
    def test_smallest_s_package_price(self, delivery:SmallestDeliveryPriceAmongProviders, transaction):
        
        delivery_data = delivery.calculate(transaction, self.customer)
        
        assert delivery_data.delivery_price == LP_S
    
    def test_s_package_price(self, delivery:SmallestDeliveryPriceAmongProviders, transaction):
        
        delivery_data = delivery.calculate(transaction, self.customer)
        
        assert delivery_data.delivery_price != MR_S
        
    def test_s_package_price_discount_value(self, delivery:SmallestDeliveryPriceAmongProviders, transaction):
        
        delivery_data = delivery.calculate(transaction, self.customer)
        
        assert delivery_data.discount == MR_S - LP_S
        
    def test_smallest_m_package_price(self, delivery:SmallestDeliveryPriceAmongProviders):
        
        transaction = Transaction(date=date(year=2020, month=10, day=25), package_size=PackageSizeEnum.M, provider=DeliveryProviderEnum.LP)
        
        delivery_data = delivery.calculate(transaction, self.customer)
        
        assert delivery_data.delivery_price == MR_M
    
    def test_smallest_l_package_price(self, delivery:SmallestDeliveryPriceAmongProviders):
        
        transaction = Transaction(date=date(year=2020, month=10, day=25), package_size=PackageSizeEnum.L, provider=DeliveryProviderEnum.LP)
        
        delivery_data = delivery.calculate(transaction, self.customer)
        
        assert delivery_data.delivery_price == MR_L