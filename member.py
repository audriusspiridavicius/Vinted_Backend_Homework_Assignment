from transaction import MemberTransaction


class Member:
    
    def __init__(self, transactions:list[MemberTransaction] = None) -> None:
        if transactions is None:
            transactions = []
        self.__transactions = transactions

    def add_transaction(self, transaction:MemberTransaction) -> None:
        self.__transactions.append(transaction)

    def display_transactions(self):
    def get_member_transactions(self):
        return self.__transactions

if __name__ == "__main__":
    
    m = Member()
    
    m.display_transactions()