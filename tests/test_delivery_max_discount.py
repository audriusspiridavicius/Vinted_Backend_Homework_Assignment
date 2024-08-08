import pytest
from tests.test_settings import delivery_rules, LP_L
from transaction import MemberTransaction, Transaction
from member import Member
from datetime import date
from enums import DeliveryProviderEnum, PackageSizeEnum
from delivery import DeliveryMaxDiscount, FreeDeliveryNTimesMonth, FreeDeliveryNthTimes, SmallestDeliveryPriceAmongProviders



@pytest.fixture
def member():
    return Member()


@pytest.fixture
def member_discount_full_price(member):
    
    member.add_transaction(MemberTransaction(date(2024, 5, 10), PackageSizeEnum.L, DeliveryProviderEnum.LP))
    member.add_transaction(MemberTransaction(date(2024, 5, 11), PackageSizeEnum.L, DeliveryProviderEnum.LP))
    return member
    
@pytest.fixture
def member_discount_part_price(member):
    
    member.add_transaction(MemberTransaction(date(2024, 5, 10), PackageSizeEnum.S, DeliveryProviderEnum.LP, price=10, discount=5))
    member.add_transaction(MemberTransaction(date(2024, 5, 11), PackageSizeEnum.S, DeliveryProviderEnum.LP, price=10, discount=2))
    member.add_transaction(MemberTransaction(date(2024, 6, 11), PackageSizeEnum.L, DeliveryProviderEnum.LP, price=10, discount=0.75))
    member.add_transaction(MemberTransaction(date(2024, 7, 11), PackageSizeEnum.L, DeliveryProviderEnum.LP, price=10, discount=2))
    return member


@pytest.fixture
def member_discount_max_reached(member):
    
    member.add_transaction(MemberTransaction(date(2024, 6, 11), PackageSizeEnum.L, DeliveryProviderEnum.LP, price=10, discount=7))
    member.add_transaction(MemberTransaction(date(2024, 7, 11), PackageSizeEnum.L, DeliveryProviderEnum.LP, price=10, discount=3))
    return member


class TestMaxDiscount:
    
    @pytest.mark.parametrize("tran_date,delivery_manager,package_size,delivery_provider",[
        (date(2024, 5, 11),FreeDeliveryNTimesMonth, PackageSizeEnum.L, DeliveryProviderEnum.LP),
        (date(2024, 6, 11),FreeDeliveryNthTimes, PackageSizeEnum.L, DeliveryProviderEnum.LP),
        ])
    def test_discount_full_price(self, member_discount_full_price, delivery_rules,
                                 tran_date, delivery_manager, package_size, delivery_provider):
        
        transaction = Transaction(tran_date, package_size, delivery_provider)
        
        delivery = DeliveryMaxDiscount(delivery_manager(delivery_rules))
        
        delivery_data = delivery.calculate(transaction, member_discount_full_price)
        
        assert delivery_data.discount == LP_L
        
    @pytest.mark.parametrize("tran_date",[(date(2024, 5, 11)), (date(2024, 6, 11)),
    ])
    def test_discount_part_price_s_smallest(self, member_discount_part_price, delivery_rules, tran_date,):
        
        transaction = Transaction(tran_date,PackageSizeEnum.S, DeliveryProviderEnum.MR)
        
        delivery = DeliveryMaxDiscount(SmallestDeliveryPriceAmongProviders(delivery_rules))
        
        delivery_data = delivery.calculate(transaction, member_discount_part_price)
        
        assert delivery_data.discount == 0.25
        
    def test_discount_part_price_L(self, member_discount_part_price, delivery_rules):
        
        transaction = Transaction(date(2024, 6, 29),PackageSizeEnum.L, DeliveryProviderEnum.LP)
        
        delivery = DeliveryMaxDiscount(FreeDeliveryNthTimes(delivery_rules))
        
        delivery_data = delivery.calculate(transaction, member_discount_part_price)
        
        assert delivery_data.discount == 0.25
        assert delivery_data.delivery_price == 6.65
        
    def test_discount_max_reached(self, member_discount_max_reached, delivery_rules):
        transaction = Transaction(date(2024, 6, 29),PackageSizeEnum.L, DeliveryProviderEnum.LP)
        
        delivery = DeliveryMaxDiscount(FreeDeliveryNthTimes(delivery_rules))
        
        delivery_data = delivery.calculate(transaction, member_discount_max_reached)
        
        assert delivery_data.discount == 0.00
        assert delivery_data.delivery_price == 6.90