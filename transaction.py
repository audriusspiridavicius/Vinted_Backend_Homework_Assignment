class Transaction:
    def __init__(self, date, package_size, provider):
        
        self.date = date
        self.package_size = package_size
        self.provider = provider
    
    def __str__(self) -> str:
        return f"{self.date} {self.package_size} {self.provider}"
    
    def __repr__(self) -> str:
        return self.__str__()

