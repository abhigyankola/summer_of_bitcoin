import sys

sys.stdout = open('block.txt', 'w') # For printing the txid directly in the file block.txt

parents_list={}

transaction_list=[]

block_size_limit = 4000000

class MempoolTransaction():

    def __init__(self, txid, fee, weight, parents):

        self.txid = txid

        self.fee = int(fee)

        self.weight = int(weight)

        self.parents = parents.split(";")

        self.chain_number = -1 # Here -1 implies that the transaaction is not involed in any chain

def parse_mempool_csv():

    """Parse the CSV file and return a list of MempoolTransactions."""

    with open('mempool.csv') as f:

        return([MempoolTransaction(*line.strip().split(',')) for line in f.readlines()[1:]])

def is_last(transaction):

    global parents_list

    if (len(transaction.parents)!=0) and (transaction.txid not in parents_list):

        if len(transaction.parents)==1 and transaction.parents[0]=="":

            return False

        return True

    return False


if __name__ == "__main__":
    
    transaction_chains=[]

    parents_list[""]=False

    transaction_list = parse_mempool_csv() 

    transaction_indices={}

    for i in range(len(transaction_list)):

        if transaction_list[i].parents!="":

            for j in transaction_list[i].parents:

                parents_list[j] = True

        transaction_indices[transaction_list[i].txid] = i
    
    priority_list = []

    index = 0

    for transaction in transaction_list:

        """To find the first transacction in the chain first we must find the last transaction in the chain.
        Using the last transaction in the chain we can reach the first block by performing DFS"""

        if transaction.chain_number==-1 and is_last(transaction):
            
            transaction.chain_number = index 

            reversed_chain = [] 

            chain_fee = transaction.fee

            chain_weight = transaction.weight

            current_transaction = transaction

            stack = [] 

            stack.append(current_transaction)

            """ Iterative Depth first search  """

            while len(stack) != 0:

                current_transaction = stack.pop()

                reversed_chain.append(current_transaction) #Storing the chain we get through DFS
    
                current_transaction.chain_number = index

                chain_fee += current_transaction.fee

                chain_weight += current_transaction.weight

                for parent in current_transaction.parents:

                    if parent!="" and transaction_list[transaction_indices[parent]].chain_number == -1:

                        stack.append(transaction_list[transaction_indices[parent]])

            
            transaction_chains.append(reversed_chain[::-1]) # Reversing the list because we started from the end

            priority_list.append([index,chain_weight,chain_fee])

            index += 1

    for transaction in transaction_list:
        
        if transaction.chain_number==-1:
    
            transaction_chains.append([transaction])

            priority_list.append([index,transaction.weight,transaction.fee])

            index+=1

    """ # sorting in descending order based on fee/weight ratio of a chain """

    priority_list = sorted(priority_list, key = lambda x: x[1]/x[2])  

    total_weight = 0

    total_cost = 0 

    for chain in priority_list:

        """ We keep adding chains only if the sum of weight of the chain and total_weight is not more than 4000000"""

        if total_weight + chain[1] <= block_size_limit:

            total_weight += chain[1]

            total_cost += chain[2]

            for transaction in transaction_chains[chain[0]]:

                print(transaction.txid)

    #print(total_cost,total_weight) 
    #Result for the given mempool file is Fee = 5997882 satoshi , Weight = 3999836
        








    

