import pytest
from datetime import date
from delivery_rule import BasicDeliveryRule
from enums import DeliveryProviderEnum, PackageSizeEnum
from transaction import Transaction, MemberTransaction
from delivery import FreeDelivery
from member import Member

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
def transactions():
    return [
        Transaction(date(2010, 5, 1), "S", "LP"),
    ]
    
@pytest.fixture
def repetetive_transaction():
    return MemberTransaction(date(2010, 5, 1), "S", "LP", 100, 0)



@pytest.fixture
def customer_with_transactions(repetetive_transaction):
    customer = Member()
    customer.add_transaction(repetetive_transaction)
    return customer

@pytest.fixture(scope="function")
def customer_without_transactions():
    c = Member()
    return c

class TestFreeDeliveryNotApplied:
    
    def test_customer_has_one_transaction(self, delivery_rules, transactions, customer_with_transactions):
        
        delivery = FreeDelivery(delivery_rules)
        
        delivary_data = delivery.calculate(transactions[0], customer_with_transactions)
        
        assert delivary_data.delivery_price != 0
        assert delivary_data.discount == 0
        
    def test_customer_has_zero_transaction(self, delivery_rules, transactions, customer_without_transactions):
        
        delivery = FreeDelivery(delivery_rules)
        
        delivary_data = delivery.calculate(transactions[0], customer_without_transactions)
        
        assert delivary_data.delivery_price != 0
        assert delivary_data.discount == 0
        
    def test_customer_has_3_same_transaction(self, delivery_rules, transactions, customer_with_transactions:Member, repetetive_transaction):
        
        delivery = FreeDelivery(delivery_rules)
        
        customer_with_transactions.add_transaction(repetetive_transaction)
        customer_with_transactions.add_transaction(repetetive_transaction)
        
        delivary_data = delivery.calculate(transactions[0], customer_with_transactions)
        
        assert delivary_data.delivery_price != 0
        assert delivary_data.discount == 0
        
    def test_customer_has_3_various_carriers_transaction(self, delivery_rules, transactions):
        
        delivery = FreeDelivery(delivery_rules)
        c = Member()
        
        c.add_transaction(MemberTransaction(date(2010, 5, 1), "M", "LP", 100, 0))
        c.add_transaction(MemberTransaction(date(2010, 5, 1), "L", "LP", 100, 0))
        c.add_transaction(MemberTransaction(date(2010, 5, 1), "S", "LP", 100, 0))
        
        delivary_data = delivery.calculate(transactions[0], c)
        
        assert delivary_data.delivery_price != 0
        assert delivary_data.discount == 0
        
    def test_nth_shipment_free_zero(self, delivery_rules, transactions, customer_with_transactions:Member):
        
        delivery = FreeDelivery(delivery_rules, nth_shipment_free=0)
        
        delivary_data = delivery.calculate(transactions[0], customer_with_transactions)
        
        assert delivary_data.delivery_price != 0
        assert delivary_data.discount == 0
        
    def test_nth_shipment_free_bigger_than_transaction_count(self, delivery_rules, transactions, customer_with_transactions:Member):
        
        delivery = FreeDelivery(delivery_rules, nth_shipment_free=100)
        
        delivary_data = delivery.calculate(transactions[0], customer_with_transactions)
        
        assert delivary_data.delivery_price != 0
        assert delivary_data.discount == 0
        
        
class TestFreeDeliveryApplied:
    
    def test_default_setting_nth_3(self, delivery_rules, customer_with_transactions, repetetive_transaction, transactions):
        
        delivery = FreeDelivery(delivery_rules)
        
        customer_with_transactions.add_transaction(repetetive_transaction) # second same transaction added
        
        delivery_data = delivery.calculate(transactions[0], customer_with_transactions)
        
        assert delivery_data.delivery_price == 0
        assert delivery_data.discount == LPS_PRICE
        
    def test_nth_shipment_free_one(self, delivery_rules, transactions, customer_with_transactions:Member):
        
        delivery = FreeDelivery(delivery_rules, nth_shipment_free=1)
        
        delivary_data = delivery.calculate(transactions[0], customer_with_transactions)
        
        assert delivary_data.delivery_price == 0
        assert delivary_data.discount != 0
        
    def test_nth_shipment_many_records(self, delivery_rules, transactions, customer_with_transactions:Member, repetetive_transaction):
        
        
        delivery = FreeDelivery(delivery_rules, nth_shipment_free=50)
        
        for _ in range(48):
            customer_with_transactions.add_transaction(repetetive_transaction)
        
        
        delivary_data = delivery.calculate(transactions[0], customer_with_transactions)
        
        assert delivary_data.delivery_price == 0
        assert delivary_data.discount != 0
    
        