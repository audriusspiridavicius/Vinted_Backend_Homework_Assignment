from transaction import Transaction
from member import Member
from enums import DeliveryProviderEnum, PackageSizeEnum
class DeliveryRule:
    
    def __init__(self, provider:DeliveryProviderEnum, size:PackageSizeEnum, price:int) -> None:
        self.provider = provider
        self.size = size
        self.price = price
        
    def check_rule(self, transaction, member):
        
        raise NotImplementedError()


class BasicDeliveryRule(DeliveryRule):
    
    def check_rule(self, transaction:Transaction, member:Member):
        if self.provider == transaction.provider and self.size == transaction.package_size:
            return True
        return False
        