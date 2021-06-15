# summer_of_bitcoin

A possible solution for the given task.
My solution mainly depends upon the fee : weight ratio and going greedy in-order to maximize the profit.
There are cases in which this may fail to give us maximum profit. 
We can get more profit using dynamic programming (knapsack problem) for this problem but the space complexity (greater than a 1GB for given mempool) and time complexity will be too high to implement on a normal PC. So, I didn't consider implementing it.
As the mempools in the real world are very large, greedy approach will be more time and space efficient which also play a part in maximizing profit.  
