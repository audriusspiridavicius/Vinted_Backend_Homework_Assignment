import pytest
from delivery import DeliveryMaxDiscountPerMonth, FreeDelivery, FreeDeliveryNthTimes, FreeDeliveryNTimesMonth, SmallestDeliveryPriceAmongProviders
from member import Member
from transaction import Transaction, MemberTransaction
from enums import DeliveryProviderEnum, PackageSizeEnum
from tests.test_settings import delivery_rules, LP_L
from datetime import date


@pytest.fixture
def member():
    return Member()

class TestDeliveryMaxDiscountPerMonthApplied:
    
    @pytest.mark.parametrize("transaction, member_transaction, delivery_manager, n", 
    [
        (
            Transaction(date(2020,1,1), PackageSizeEnum.M, DeliveryProviderEnum.MR),
            [
                MemberTransaction(date(2020,1,1), PackageSizeEnum.M, DeliveryProviderEnum.MR, price=5),
                MemberTransaction(date(2020,1,2), PackageSizeEnum.M, DeliveryProviderEnum.MR, price=100),
            ],
            FreeDelivery,
            3
        ),
        (
            Transaction(date(2020,1,1), PackageSizeEnum.S, DeliveryProviderEnum.LP),
            [
                MemberTransaction(date(2021,10,1), PackageSizeEnum.S, DeliveryProviderEnum.LP, price=5),
                MemberTransaction(date(2021,10,2), PackageSizeEnum.S, DeliveryProviderEnum.LP, price=100),
                MemberTransaction(date(2021,10,2), PackageSizeEnum.S, DeliveryProviderEnum.LP, price=200),
            ],
            FreeDeliveryNthTimes,
            4
        )
    ]                         
    )
    def test_discount_applied(self, member, transaction, member_transaction, delivery_rules, delivery_manager, n):
        
        self.add_member_transactions(member, member_transaction)
        delivery = DeliveryMaxDiscountPerMonth(delivery_manager(delivery_rules, n))
        delivery_data = delivery.calculate(transaction, member)
        
        assert delivery_data.delivery_price == 0
        

    def test_disount_applied_different_months(self, member, delivery_rules):
        transaction = Transaction(date(2019, 6, 6), PackageSizeEnum.L, DeliveryProviderEnum.LP)
        
        member_transactions = [
            MemberTransaction(date(2019, 5, 6), PackageSizeEnum.L, DeliveryProviderEnum.LP, price=10, discount=5),
            MemberTransaction(date(2019, 5, 6), PackageSizeEnum.L, DeliveryProviderEnum.LP, price=5, discount=5),
            MemberTransaction(date(2019, 6, 1), PackageSizeEnum.L, DeliveryProviderEnum.LP, price=5),
            MemberTransaction(date(2019, 6, 2), PackageSizeEnum.L, DeliveryProviderEnum.LP, price=5),
        ]
        
        
        self.test_discount_applied(member, transaction, member_transactions, delivery_rules, FreeDeliveryNTimesMonth, 3)
    
    def test_discount_applied_different_years(self, member, delivery_rules):
        transaction = Transaction(date(2020, 5, 6), PackageSizeEnum.L, DeliveryProviderEnum.LP)
        
        member_transactions = [
            MemberTransaction(date(2019, 5, 6), PackageSizeEnum.L, DeliveryProviderEnum.LP, price=10, discount=5),
            MemberTransaction(date(2019, 5, 6), PackageSizeEnum.L, DeliveryProviderEnum.LP, price=5, discount=5),
            MemberTransaction(date(2020, 5, 1), PackageSizeEnum.L, DeliveryProviderEnum.LP, price=5),
            MemberTransaction(date(2020, 5, 2), PackageSizeEnum.L, DeliveryProviderEnum.LP, price=5),
        ]
        
        self.test_discount_applied(member, transaction, member_transactions, delivery_rules, FreeDeliveryNTimesMonth, 3)
    
    
    
    @pytest.mark.parametrize("member_transactions, transaction, expected_discount, delivery_manager", [
        ([MemberTransaction(date(2020, 10, 11), PackageSizeEnum.S, DeliveryProviderEnum.LP, price=5, discount=9)],
         Transaction(date(2020, 10, 11), PackageSizeEnum.L, DeliveryProviderEnum.MR), 0, SmallestDeliveryPriceAmongProviders),
        ([MemberTransaction(date(2000, 5, 5), PackageSizeEnum.S, DeliveryProviderEnum.LP, price=5, discount=5)],
         Transaction(date(2000, 5, 5), PackageSizeEnum.L, DeliveryProviderEnum.LP), 2.9, SmallestDeliveryPriceAmongProviders),
        ([MemberTransaction(date(2000, 1, 5), PackageSizeEnum.S, DeliveryProviderEnum.LP, price=5, discount=9)],
         Transaction(date(2000, 1, 15), PackageSizeEnum.M, DeliveryProviderEnum.LP), 1, SmallestDeliveryPriceAmongProviders),
        ([MemberTransaction(date(2000, 1, 5), PackageSizeEnum.S, DeliveryProviderEnum.LP, price=5, discount=9),
          MemberTransaction(date(2000, 1, 10), PackageSizeEnum.S, DeliveryProviderEnum.LP, price=5)],
         Transaction(date(2000, 1, 15), PackageSizeEnum.S, DeliveryProviderEnum.LP), 1, FreeDelivery)
    ])
    def test_discount_applied_partially(self, member,  delivery_rules, member_transactions, transaction, expected_discount, delivery_manager):
        
        self.add_member_transactions(member, member_transactions)
        
        delivery = DeliveryMaxDiscountPerMonth(delivery_manager(delivery_rules))
        delivery_data = delivery.calculate(transaction, member)
        
        assert delivery_data.discount == expected_discount

    
    @pytest.mark.parametrize("transaction1, transaction2, member_transactions, expected_discount_full, expected_discount_partial",
    [
        (
            Transaction(date(2020, 1, 1), PackageSizeEnum.L, DeliveryProviderEnum.LP), Transaction(date(2020, 1, 2), PackageSizeEnum.L, DeliveryProviderEnum.LP),
            [MemberTransaction(date(2020, 1, 1), PackageSizeEnum.L, DeliveryProviderEnum.LP), MemberTransaction(date(2020, 1, 10), PackageSizeEnum.L, DeliveryProviderEnum.LP)],
            6.9, 3.1
        ),
        (
            Transaction(date(2020, 1, 1), PackageSizeEnum.L, DeliveryProviderEnum.LP), Transaction(date(2020, 1, 2), PackageSizeEnum.L, DeliveryProviderEnum.MR),
            [MemberTransaction(date(2020, 1, 1), PackageSizeEnum.L, DeliveryProviderEnum.LP), MemberTransaction(date(2020, 1, 10), PackageSizeEnum.L, DeliveryProviderEnum.LP)],
            6.9, 3.1
        )
    ])
    def test_discount_applied_fully_and_partially(self, member, transaction1, transaction2, member_transactions, expected_discount_full, expected_discount_partial, delivery_rules):
        self.add_member_transactions(member, member_transactions)
        
        delivery = DeliveryMaxDiscountPerMonth(FreeDeliveryNTimesMonth(delivery_rules,3,2))
        delivery_data = delivery.calculate(transaction1, member)
        self.add_member_transactions(member, [MemberTransaction(**transaction1.__dict__, price=delivery_data.delivery_price, discount=delivery_data.discount)])
        
        assert delivery_data.discount == expected_discount_full
        
        self.add_member_transactions(member, [MemberTransaction(**transaction2.__dict__), MemberTransaction(**transaction2.__dict__)])
        
        
        delivery_data_next_transaction = delivery.calculate(transaction2, member)
        assert delivery_data_next_transaction.discount == expected_discount_partial
    
    
    def add_member_transactions(self, member:Member, transactions:list[MemberTransaction]):
        for transaction in transactions:
            member.add_transaction(transaction)
    

@pytest.fixture
def member_transactions():
    return [
        MemberTransaction(date(2024, 3,3), PackageSizeEnum.L, DeliveryProviderEnum.LP, price=1, discount=5),
        MemberTransaction(date(2024, 3,20), PackageSizeEnum.L, DeliveryProviderEnum.LP, price=1, discount=4),        
        MemberTransaction(date(2024, 3,21), PackageSizeEnum.M, DeliveryProviderEnum.MR, price=1, discount=1),        
    ]

@pytest.fixture
def member_discount_exeeded(member_transactions):
    
    return Member(member_transactions)
    

class TestDeliveryMaxDiscountPerMonthExeeded:
    
    def test_free_nth_delivery(self, member_discount_exeeded, delivery_rules):
        
        transaction = Transaction(date(2024, 3, 25), PackageSizeEnum.L, DeliveryProviderEnum.LP)
        
        delivery = DeliveryMaxDiscountPerMonth(FreeDelivery(delivery_rules, 3))
        
        delivery_data = delivery.calculate(transaction, member_discount_exeeded)
        
        assert delivery_data.discount == 0
        assert delivery_data.delivery_price == LP_L
    
    def test_free_nth_delivery_n_times(self, delivery_rules, member_discount_exeeded):
        transaction = Transaction(date(2024, 3, 25), PackageSizeEnum.L, DeliveryProviderEnum.LP)
        
        delivery = DeliveryMaxDiscountPerMonth(FreeDeliveryNthTimes(delivery_rules, 3))
        
        delivery_data = delivery.calculate(transaction, member_discount_exeeded)
        
        assert delivery_data.discount == 0
        assert delivery_data.delivery_price == LP_L
    
    def test_free_nth_delivery_n_times_per_month(self, delivery_rules, member_discount_exeeded):
        transaction = Transaction(date(2024, 3, 25), PackageSizeEnum.L, DeliveryProviderEnum.LP)
        
        delivery = DeliveryMaxDiscountPerMonth(FreeDeliveryNTimesMonth(delivery_rules, 3))
        
        delivery_data = delivery.calculate(transaction, member_discount_exeeded)
        
        assert delivery_data.discount == 0
        assert delivery_data.delivery_price == LP_L