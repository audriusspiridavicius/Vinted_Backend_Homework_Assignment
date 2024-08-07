import pytest
from datetime import date
from member import Member
from transaction import Transaction, MemberTransaction
from enums import DeliveryProviderEnum, PackageSizeEnum
from test_settings import delivery_rules
from delivery import FreeDeliveryNTimesMonth


@pytest.fixture
def transactions():
    return [
        MemberTransaction(date(2020, 10, 11), PackageSizeEnum.S, DeliveryProviderEnum.LP),
        MemberTransaction(date(2020, 10, 12), PackageSizeEnum.S, DeliveryProviderEnum.LP),
        MemberTransaction(date(2020, 10, 13), PackageSizeEnum.S, DeliveryProviderEnum.LP),
    ]
@pytest.fixture
def member(transactions):
    return Member(transactions)


@pytest.fixture
def add_transaction():
    return Transaction(date(2020, 10, 25), PackageSizeEnum.S, DeliveryProviderEnum.LP)

class TestFreeDeliveryNTimesMonthApplied:
    
    def test_multiple_times_per_month(self, add_transaction, delivery_rules):
        m = Member()
        m.add_transaction(MemberTransaction(**add_transaction.__dict__))
        
        delivery = FreeDeliveryNTimesMonth(delivery_rules, 2, 2)
        
        delivery_data = delivery.calculate(add_transaction, m)
        
        assert delivery_data.delivery_price == 0
        
        m.add_transaction(MemberTransaction(**add_transaction.__dict__))
        m.add_transaction(MemberTransaction(**add_transaction.__dict__))
        
        delivery_data = delivery.calculate(add_transaction, m)
        
        assert delivery_data.delivery_price == 0
    
    @pytest.mark.parametrize("month",[1,2,3,4,5,7,6,8,9,11,12])
    def test_month_once(self, member:Member, delivery_rules, month):
        
        delivery = FreeDeliveryNTimesMonth(delivery_rules, 4, 1)
        
        tr = Transaction(date(2020, 10, 20), PackageSizeEnum.S, DeliveryProviderEnum.LP)
        delivery_data = delivery.calculate(tr, member)
        member.add_transaction(MemberTransaction(**tr.__dict__, price=delivery_data.delivery_price, discount=delivery_data.discount))
        
        assert delivery_data.delivery_price == 0
        
        for day in range(1,4):
            member.add_transaction(MemberTransaction(date(2020, month, day), PackageSizeEnum.S, DeliveryProviderEnum.LP))
        
        delivery_data_next_month = delivery.calculate(Transaction(date(2020, month, 4), PackageSizeEnum.S, DeliveryProviderEnum.LP), member)
        assert delivery_data_next_month.delivery_price == 0
        