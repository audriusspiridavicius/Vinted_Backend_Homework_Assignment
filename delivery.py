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


class FreeDelivery(Delivery):
    
    def __init__(self, delivery_rules: list[DeliveryRule], nth_shipment_free:int = 3) -> None:
        
        self.nth_shipment_free = nth_shipment_free
        super().__init__(delivery_rules)
    
    
    def calculate(self, transaction: Transaction, member: Member) -> DeliveryData:
        
        d_data = super().calculate(transaction, member)

        shipment_count = self._get_shipment_count(transaction, member)
        
        if self.nth_shipment_free > 0 and shipment_count > 0 and ((shipment_count + 1) % self.nth_shipment_free == 0):
            d_data.discount = d_data.delivery_price
            d_data.delivery_price = 0
        
        return d_data
    
    
    def _get_shipment_count(self, transaction: Transaction, member: Member):
        
        shipment_count = 0
        for member_transaction in member.get_member_transactions():
            if member_transaction.package_size == transaction.package_size and member_transaction.provider == transaction.provider:
                shipment_count += 1
        return shipment_count

    
class FreeDeliveryNthTimes(FreeDelivery):
    
    def __init__(self, delivery_rules: list[DeliveryRule], nth_shipment_free: int = 3, nth_times = 1) -> None:
        super().__init__(delivery_rules, nth_shipment_free)
        self.nth_times = nth_times
    
    
    def calculate(self, transaction: Transaction, member: Member) -> DeliveryData:
        
        shipment_count = self._get_shipment_count(transaction, member)
        
        if shipment_count < self.nth_shipment_free * self.nth_times:
            return super().calculate(transaction, member)
        
        return Delivery.calculate(self, transaction, member)
        
