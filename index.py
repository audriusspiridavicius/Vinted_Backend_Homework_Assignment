from delivery_rule import BasicDeliveryRule
from delivery import Delivery
from member import Member
from transaction_provider import TransactionsFromTextFile
from enums import DeliveryProviderEnum, PackageSizeEnum
from delivery_manager_provider import DeliveryManagerProvider
from transaction import MemberTransaction

def get_regular_delivery_rules():
    delivery_rules = [
        BasicDeliveryRule(DeliveryProviderEnum.LP, PackageSizeEnum.S, 1.50),
        BasicDeliveryRule(DeliveryProviderEnum.LP, PackageSizeEnum.M, 4.90),
        BasicDeliveryRule(DeliveryProviderEnum.LP, PackageSizeEnum.L, 6.90),
        
        BasicDeliveryRule(DeliveryProviderEnum.MR, PackageSizeEnum.S, 2),
        BasicDeliveryRule(DeliveryProviderEnum.MR, PackageSizeEnum.M, 3),
        BasicDeliveryRule(DeliveryProviderEnum.MR, PackageSizeEnum.L, 4),
        
    ]
    
    return delivery_rules



if __name__ == "__main__":
    
    customer = Member()
    
    transaction_provider = TransactionsFromTextFile()
    
    transactions = transaction_provider.get_transactions()
    
    
    delivery_rules = get_regular_delivery_rules()
    
    
    for transaction in transactions:
        if not transaction.ignored:
            delivery_manger = DeliveryManagerProvider(transaction, customer, delivery_rules)
            
            delivery_calculation_manager = delivery_manger.get_manager()
            delivery_data = delivery_calculation_manager.calculate(transaction, customer)
            
            customer.add_transaction(MemberTransaction(**transaction.__dict__, price=delivery_data.delivery_price, discount=delivery_data.discount))
        else:
            customer.add_transaction(MemberTransaction(**transaction.__dict__, price="Ignored"))
    customer.display_transactions()
    