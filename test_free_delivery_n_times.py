import pytest
from datetime import date
from delivery import FreeDeliveryNthTimes
from delivery_rule import BasicDeliveryRule
from member import Member
from transaction import Transaction, MemberTransaction
from enums import PackageSizeEnum, DeliveryProviderEnum

test_date = date(2010, 11, 10)
LPS_PRICE = 1
LPM_PRICE = 2.99
LPL_PRICE = 10


@pytest.fixture
def delivery_rules():
    
    return [
        BasicDeliveryRule(DeliveryProviderEnum.LP, PackageSizeEnum.S, LPS_PRICE),
        BasicDeliveryRule(DeliveryProviderEnum.LP, PackageSizeEnum.M, LPM_PRICE),
        BasicDeliveryRule(DeliveryProviderEnum.LP, PackageSizeEnum.L, LPL_PRICE),
    ]
@pytest.fixture
def member_transactions():
    return [
        MemberTransaction(test_date, PackageSizeEnum.L, DeliveryProviderEnum.LP),
        MemberTransaction(test_date, PackageSizeEnum.L, DeliveryProviderEnum.LP),
    ]

@pytest.fixture
def member(member_transactions):
    m = Member(member_transactions)
    return m

@pytest.fixture
def transaction():
    return Transaction(test_date, PackageSizeEnum.L, DeliveryProviderEnum.LP)

class TestFreeDeliveryNTimesApplied:
    
    def test_applied_once(self, member, transaction, delivery_rules):
        
        d = FreeDeliveryNthTimes(delivery_rules)
        
        d_data = d.calculate(transaction, member)
        
        d_data.delivery_price == 0
        
        
    
    def test_applied_multiple_times(self, member:Member, transaction:Transaction, delivery_rules):
        
        d = FreeDeliveryNthTimes(delivery_rules, nth_times=2)
        d_data = d.calculate(transaction, member)
        member.add_transaction(MemberTransaction(**transaction.__dict__))
        assert d_data.delivery_price == 0
        
        member.add_transaction(MemberTransaction(**transaction.__dict__))
        member.add_transaction(MemberTransaction(**transaction.__dict__))
    
        d_data = d.calculate(transaction, member)
        assert d_data.delivery_price == 0
    
    
class TestFreeDeliveryNTimesNotApplied:
    
    @pytest.mark.parametrize("n_time", [1, 2, 3, 5, 50, 100])
    def test_member_has_no_transactions(self, transaction, delivery_rules,n_time):
        
        m = Member()
        
        d = FreeDeliveryNthTimes(delivery_rules, nth_times=n_time)
        
        delivery_data = d.calculate(transaction, m)
        
        assert delivery_data.delivery_price == LPL_PRICE
        assert delivery_data.discount == 0
        
    def test_free_once(self, transaction, delivery_rules):
        
        m = Member()
        m.add_transaction(MemberTransaction(**transaction.__dict__))
        m.add_transaction(MemberTransaction(**transaction.__dict__))
        m.add_transaction(MemberTransaction(**transaction.__dict__))
        
        d = FreeDeliveryNthTimes(delivery_rules, nth_shipment_free=2, nth_times=1)
        
        delivery_data = d.calculate(transaction, m)
        
        assert delivery_data.delivery_price == LPL_PRICE
        assert delivery_data.discount == 0
        
    # def test_n_over_nth_times