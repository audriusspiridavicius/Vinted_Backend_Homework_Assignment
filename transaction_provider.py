import os
from transaction import Transaction
import datetime


class TransactionProvider:
    
    def get_transactions(self) -> list[Transaction]:
        """get transactions data"""
        
        raise NotImplementedError()


class TransactionsFromTextFile(TransactionProvider):
    
    def get_transactions(self, filename="input.txt") -> list[Transaction]:
        """get transactions data from text file"""
        transactions = []
        if os.path.exists(filename):
            with open(filename, "r") as file:
                transaction_lines = file.readlines()
                for transaction_line in transaction_lines:
                    transaction_data = transaction_line.strip().split()
                    transaction_data = {index:tran for index, tran in enumerate(transaction_data)}
                    
                    transaction_date = transaction_data.get(0, "")
                    transaction_date = datetime.date.fromisoformat(transaction_date)
                    
                    transactions.append(
                        Transaction(
                            date=transaction_date,
                            package_size=transaction_data.get(1, ""),
                            provider=transaction_data.get(2, "")
                        )
                    )
                
        return transactions

        
if __name__ == "__main__":
    pass
    