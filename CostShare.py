from decimal import Decimal, ROUND_DOWN

class _Person:
    def __init__(self, name):
        """"Private class. """
        # Person keeps track of their own name and their balance: (+)credit (-)debt
        self._name = name
        self._balance = 0

class Group:
    def __init__(self):
        """ Creates an empty group to which people can be added."""
        self._members = {} # key:values are name{str}:_Person instance

    def addPerson(self, name:str):
        """ Creates a new person in the group that can:
            - Be passed as payer and payee for transactions.
            - Hold a personal balance; a real number that is positive for creditors and negative for debtors.
            Two people can not have the same name. """

        if not isinstance(name, str): # Error management
            raise ValueError('Input argument should be a name {str}')

        newPerson = _Person(name) # Creates a person with the provided name
        self._members[name] = newPerson # Maps the persons name to their _Person instance in the group dictionary

    def numberOfPeople(self):
        """ Returns the number of people in the group as an integer. """

        return len(self._members)

    def listOfPeople(self):
        """ Returns a list of names of all people currently in the group. """

        listOfPeople = []
        for name in self._members:
            listOfPeople.append(name)
        return listOfPeople

    def returnDebt(self, namesToCheck:str or list):
        """ Takes in people argument as a single person or a list of people and returns a list containing their personal balances."""

        debtArray = []
        if not isinstance(namesToCheck, list): # Segment converts single name to list of names
            namesToCheck = [namesToCheck]

        for name in namesToCheck:
            debtArray.append(self._members[name]._balance)
        return debtArray

    def addExpense(self, payees: str or list, payers: str or list, cost: int, payeeSplit: str or list = None,
                   payerSplit: str or list = None):
        """ Adds an expense within a group. Takes in payees, payers, price, and (optional) payees and payers split.
        - Person arguments (payees and payers) can be passed as single names {str} or list {list} containing several names.
        All people must be part of the same group.
        - Cost argument must be passed as an integer greater than 0
        - Split arguments allow for splitting the credit and debt among payees and payers. Split arguments must be passed as lists.
        Elements in the list are numbers greater than 0 that give the credit/debt share in % of the corresponding person in the person list.
        The elements must sum to 100. If no splits are passed, the credit and debt will be divided equally among payees and payers. """

        if not isinstance(payees, list): # Segment converts single name to list of name
            payees = [payees]
        if not isinstance(payers, list):
            payers = [payers]

        if payeeSplit: # Segment checks splits for correct input and formats split lists correctly
            if not sum(payeeSplit) == 100 or not len(payees) == len(payeeSplit):
                raise ValueError('Incorrectly formated payee split.')
        else:
            payeeSplit = [100/len(payees)] * len(payees)
        if payerSplit:
            if not sum(payerSplit) == 100 or not len(payers) == len(payerSplit):
                raise ValueError('Incorrectly formated payer split')
        else:
            payerSplit = [100/len(payers)] * len(payers)

        payeeCounter = 0
        for payee in payees:
            self._members[payee]._balance -= float(Decimal(str(cost * payeeSplit[payeeCounter]/100)).quantize(Decimal('0.01'), rounding=ROUND_DOWN))
            payeeCounter += 1

        payerCounter = 0
        for payer in payers:
            self._members[payer]._balance +=  float(Decimal(str(cost * payerSplit[payerCounter]/100)).quantize(Decimal('0.01'), rounding=ROUND_DOWN))


    def settleDebt(self):
        """ Returns a dictionary where each person in the group is a key. Each key is mapped to another dictionary where each person
        is a key. These keys are mapped to values of how much the initial person should receive (value > 0) from and pay (value < 0) to
        the key. Calling this method zeros all debt in the group, resetting all internal debts. """

        debtDict = {}
        debtors = []
        creditors = []

        for member in self._members:
            debtDict[member] = {}
            for member2 in self._members:
                if member2 != member:
                    debtDict[member][member2] = 0

        for member in self._members: # Makes a list of creditors and a list of debtors.
            if self._members[member]._balance > 0:
                creditors.append(member)
            if self._members[member]._balance < 0:
                debtors.append(member)

        for currentCreditor in creditors:
            while self._members[currentCreditor]._balance > 0: # While current creditor still has credit to 'hand out'.
                for currentDebtor in debtors:
                    if self._members[currentDebtor]._balance < 0: # Goes through debtors that are still holding debt.
                        if self._members[currentCreditor]._balance >= -1*self._members[currentDebtor]._balance:
                            debtDict[currentCreditor][currentDebtor] += -1*self._members[currentDebtor]._balance
                            debtDict[currentDebtor][currentCreditor] += float(self._members[currentDebtor]._balance)
                            self._members[currentCreditor]._balance -= -1*self._members[currentDebtor]._balance
                            self._members[currentDebtor]._balance = 0
                        else:
                            debtDict[currentCreditor][currentDebtor] += self._members[currentCreditor]._balance
                            debtDict[currentDebtor][currentCreditor] -= self._members[currentCreditor]._balance
                            self._members[currentDebtor]._balance += self._members[currentCreditor]._balance
                            self._members[currentCreditor]._balance = 0

        return debtDict

def testingFunction():
    ### Code below tests behavior of an empty group

    EmptyGroup = Group()

    assert EmptyGroup.numberOfPeople() == 0
    assert EmptyGroup.listOfPeople() == []

    ### Code below tests class Group and methods returnDebt, numberOfPeople

    FriendGroup = Group()
    FriendGroup.addPerson('George')
    FriendGroup.addPerson('Michael')
    FriendGroup.addPerson('Frederick')
    FriendGroup.addPerson('Samuel')

    assert FriendGroup.returnDebt(['George', 'Michael', 'Frederick', 'Samuel']) == [0, 0, 0, 0]
    assert FriendGroup.numberOfPeople() == 4
    assert FriendGroup.listOfPeople() == ['George', 'Michael', 'Frederick', 'Samuel']

    ### Code below tests method addExpense

    FriendGroup.addExpense('George', ['Michael', 'Frederick', 'Samuel'], 300)
    for name in ['Michael', 'Frederick', 'Samuel']:
        assert FriendGroup._members[name]._balance == 100
    assert FriendGroup._members['George']._balance == -300

    FriendGroup.addExpense(['Michael', 'Frederick', 'Samuel'], 'George', 600)
    for name in ['Michael', 'Frederick', 'Samuel']:
        assert FriendGroup._members[name]._balance == -100
    assert FriendGroup._members['George']._balance == 300

    ### Code below tests usage of split list and method settleDebt
    settleGroup = Group()
    settleGroup.addPerson('Ann')
    settleGroup.addPerson('Li')
    settleGroup.addPerson('Mia')
    settleGroup.addPerson('Tor')
    settleGroup.addPerson('Jo')
    settleGroup.addPerson('My')
    settleGroup.addPerson('Fia')

    settleGroup.addExpense(['Ann', 'Li', 'Mia', 'Tor', 'Jo'], ['My', 'Fia'], 1000, [10, 10, 10, 10, 60])
    answerDict = settleGroup.settleDebt()
    assert(answerDict['Ann'] == {'Li': 0, 'Mia': 0, 'Tor': 0, 'Jo': 0, 'My': -100.0, 'Fia': 0})
    assert(answerDict['Fia'] == {'Ann': 0, 'Li': 0, 'Mia':0, 'Tor': 0, 'Jo': 500.0, 'My': 0})
    assert(answerDict['Jo'] == {'Ann': 0, 'Li': 0, 'Mia': 0, 'Tor': 0, 'My': -100.0, 'Fia': -500.0})

def main():
    testingFunction()

main()