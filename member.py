from transaction import MemberTransaction


class Member:
    
    __transactions:list[MemberTransaction] = []

    def add_transaction(self, transaction:MemberTransaction) -> None:
        self.__transactions.append(transaction)

    def display_transactions(self):
        print("dispay member transactions")

if __name__ == "__main__":
    
    m = Member()
    
    m.display_transactions()