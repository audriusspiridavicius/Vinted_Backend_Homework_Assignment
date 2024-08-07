from transaction import MemberTransaction
from datetime import date

class Member:
    
    def __init__(self, transactions:list[MemberTransaction] = None) -> None:
        if transactions is None:
            transactions = []
        self.__transactions = transactions

    def add_transaction(self, transaction:MemberTransaction) -> None:
        self.__transactions.append(transaction)

    def display_transactions(self):
        
        for tran in self.__transactions:
            print(tran)
            
    def get_member_transactions(self):
        return self.__transactions
    
    def get_transactions(self, start_date:date, end_date:date):
        return [tran for tran in self.__transactions if start_date <= tran.date <= end_date]

if __name__ == "__main__":
    
    m = Member()
    
    m.display_transactions()