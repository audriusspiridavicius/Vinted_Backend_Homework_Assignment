from enums import PackageSizeEnum, DeliveryProviderEnum
import datetime


class Transaction:
    def __init__(self, date:datetime.date, package_size:str, provider:str, ignored = False):
        self.ignored = ignored

        self.date = date
        self._package_size = package_size
        self._provider = provider
        
    
    @property
    def package_size(self):
        return PackageSizeEnum.__members__.get(self._package_size, self._package_size) 
    
    @property
    def provider(self):
        return DeliveryProviderEnum.__members__.get(self._provider, self._provider) 
    
    @property
    def date(self):
        return self._date
    
    @date.setter
    def date(self, date_value):
        if isinstance(date_value, str):
            try:
                self._date = datetime.date.fromisoformat(date_value)
            except:
                self.ignored = True
                self._date = date_value
        else:
            self._date = date_value
    def __str__(self) -> str:
        return f"{self.date} {f"{self.package_size.name} " if isinstance(self.package_size, PackageSizeEnum) else f"{self.package_size}"}{f'{self.provider.name}' if isinstance(self.provider, DeliveryProviderEnum) else self.provider}"
    
    def __repr__(self) -> str:
        return self.__str__()

    
class MemberTransaction(Transaction):
    def __init__(self, _date:datetime.date, _package_size:str, _provider:str, ignored:bool = False, price = 0, discount = 0):
        super().__init__(_date, _package_size, _provider, ignored)
        self.price = price
        self.discount = discount
    
    def __str__(self) -> str:
        return f"{super().__str__()} {format(self.price,".2f") if self.price != "Ignored" else self.price} {format(self.discount,".2f") if self.discount > 0 else ("" if self.price == "Ignored" else '-')}"