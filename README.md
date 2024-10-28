# CostShare: Keep track of expenses easily as a group!

### Python data structure for group expenses and member-to-member credit and debt.

A data structure that allows users to add members to a group, add group expenses and keep track of debt between members.
Can settle the debt within the group and tells the user how much each member should pay (or receive) and to whom.

### Installation

With python 3, download the CostShare.py file and run commands from terminal according to syntax described by API.

### Documentation

#### class _New Group_
    class Group:

Creates an empty group to which people can be added.  

#### Method _Add Person_
    method addPerson(self, name)
Creates a new person in the group that can:
- Be passed as payer and payee for transactions.
- Hold a personal balance; a real number that is positive for creditors and negative for debtors. 

#### Method _Add Expense_
    method addExpense(self, payees, payers, price, payeeSplit, payerSplit)
Adds a new expense that the group has taken on. Takes in payees, payers, price, and (optional) payees and payers split.

- Person arguments (payees and payers) can be passed as single names, or array containing several names.
- Cost argument must be passed as a number greater than 0
- Split arguments allow for splitting the credit and debt among payees and payers. Split arguments must be passed as arrays. Their
                    length must be the same as the corresponding people arguments and the elements must all be whole numbers greater than 0 that
                    sum to 100. If no splits are passed, the credit and debt will be divided equally among payees and payers. 

#### Method _Return Debt_
    method returnDebt(self, people):

Takes in people argument as a single person or a list of people and returns a list containing their current personal balances. 

#### Method _Number of People_
    method numberOfPeople(self):

Returns the current number of people in the group as a integer.

#### Method _List of People_
    method listOfPeople(self):

Returns a list of all the people currently in the group. 

#### Method _Settle Debt_
    method settleDebt(self):

Settles the groups internal debt between the members. Returns a dictionary with payment information detailing
how much each person should pay and receive to/from each other person. 


### Roadmap

- The API of this library will not be changed unless to deal with issues that can't be resolved in any other way. 
- Version numbers follow semantic versioning. 
