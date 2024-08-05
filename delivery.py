from delivery_data import DeliveryData
from delivery_rule import DeliveryRule
from member import Member
from transaction import Transaction

class Delivery:
    
    _delivery_price = 0
    _discount = 0
    
    def __init__(self, delivery_rules:list[DeliveryRule]) -> None:
        self.delivery_rules = delivery_rules
    
    
    def calculate(self,transaction:Transaction, member:Member) -> DeliveryData:
        self._calculate(transaction, member)
        
        # delivery discount manager functionality here ??
        
        delivery_data = DeliveryData()
        delivery_data.delivery_price = self._delivery_price
        # member.add_transaction(transaction=MemberTransaction(**transaction.__dict__, price=self._delivery_price))
        
        return delivery_data
        
            
    def _calculate(self,transaction:Transaction, member:Member):
                
        for rule in self.delivery_rules:
            # if rule.provider == transaction.provider and rule.size == transaction.package_size:
            if rule.check_rule(transaction, member):
                self._delivery_price = rule.price
                break
        else:

            self._delivery_price = "Ignored"


class SmallestDeliveryPriceAmongProviders(Delivery):
    
    
    def calculate(self, transaction: Transaction, member: Member):
        min_delivery_price = float("inf")
        
        for rule in self.delivery_rules:
            if rule.size == transaction.package_size and rule.price < min_delivery_price:
                min_delivery_price = rule.price
                
            if rule.check_rule(transaction, member):
                self._delivery_price = rule.price
                
        self._discount = self._delivery_price - min_delivery_price
        self._delivery_price = self._delivery_price - self._discount
        
        
        return DeliveryData(delivery_price=self._delivery_price, discount=self._discount)
       