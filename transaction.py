from enums import PackageSizeEnum, DeliveryProviderEnum
import datetime


class Transaction:
    def __init__(self, date:datetime.date, package_size:str, provider:str):
        
        self.date = date
        self._package_size = package_size
        self._provider = provider
    
    @property
    def package_size(self):
        return PackageSizeEnum.__members__.get(self._package_size, self._package_size) 
    
    @property
    def provider(self):
        return DeliveryProviderEnum.__members__.get(self._provider, self._provider) 
    
    
    def __str__(self) -> str:
        return f"{self.date} {self.package_size.name if isinstance(self.package_size, PackageSizeEnum) else self.package_size}{f' {self.provider.name}' if isinstance(self.provider, DeliveryProviderEnum) else self.provider}"
    
    def __repr__(self) -> str:
        return self.__str__()

    
class MemberTransaction(Transaction):
    def __init__(self, date:datetime.date, _package_size:str, _provider:str, price = 0, discount = 0):
        super().__init__(date, _package_size, _provider)
        self.price = price
        self.discount = discount
    
    def __str__(self) -> str:
        return f"{super().__str__()} {self.price} {self.discount if self.discount > 0 else ("" if self.price == "Ignored" else '-')}"