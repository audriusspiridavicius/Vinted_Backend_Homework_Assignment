from transaction import MemberTransaction


class Member:
    
    __transactions:list[MemberTransaction] = []

    def add_transaction(self, transaction:MemberTransaction) -> None:
        self.__transactions.append(transaction)

    def display_transactions(self):
    def get_member_transactions(self):
        return self.__transactions

if __name__ == "__main__":
    
    m = Member()
    
    m.display_transactions()