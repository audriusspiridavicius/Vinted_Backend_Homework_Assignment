from transaction import Transaction
from member import Member
from enums import PackageSizeEnum
from delivery import SmallestDeliveryPriceAmongProviders, Delivery
from delivery_rule import DeliveryRule


class DeliveryManagerProvider:
    
    def __init__(self,transaction:Transaction, customer:Member, delivery_rules:list[DeliveryRule]) -> None:
        self.transaction = transaction
        self.customer = customer
        self.delivery_rules = delivery_rules
    
    
    def get_manager(self) -> Delivery:
        
        delivery_manager = Delivery(self.delivery_rules)
        
        if self.transaction.package_size == PackageSizeEnum.S:
            delivery_manager = SmallestDeliveryPriceAmongProviders(self.delivery_rules)
        
        return DeliveryMaxDiscountPerMonth(delivery_manager)
    