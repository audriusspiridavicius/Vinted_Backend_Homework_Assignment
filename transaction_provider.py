from transaction import Transaction

class TransactionProvider:
    
    def get_transactions(self) -> list[Transaction]:
        """get transactions data"""
        
        raise NotImplementedError()
