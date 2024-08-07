class DeliveryData:
    
    
    
    @property
    def discount(self):
        return self._discount
    
    @property
    def delivery_price(self):
        return self._delivery_price
    
    
    @discount.setter
    def discount(self, value):
        self._discount = round(value, 2)
        
    @delivery_price.setter
    def delivery_price(self, value):
        if isinstance(value, int) or isinstance(value, float):
            self._delivery_price = round(value, 2)
        else:
            self._delivery_price = value
            
    def __init__(self, delivery_price:float = 0, discount:float = 0) -> None:
        self.delivery_price = delivery_price
        self.discount = discount
    