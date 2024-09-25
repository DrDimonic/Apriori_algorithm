from itertools import combinations
from collections import defaultdict

def apriori(filename, min_support):
    # Step 1: Read file and store transactions
    transactions = []
    with open(filename, 'r') as file:
        for line in file:
            transaction = line.strip().split()
            transactions.append(transaction)

    total_transactions = len(transactions)

    # Step 2: Calculate minimum support count
    min_support_count = (min_support / 100) * total_transactions

    # Step 3: Generate candidate 1-itemsets (C1)
    item_counts = defaultdict(int)
    for transaction in transactions:
        for item in transaction:
            item_counts[(item,)] += 1

    # Step 4: Filter candidate itemsets to get L1 (frequent 1-itemsets)
    L1 = {itemset: count for itemset, count in item_counts.items() if count >= min_support_count}
    frequent_itemsets = L1.copy()

    # Step 5: Generate larger itemsets (Ck -> Lk)
    k = 2
    while L1:
        # Generate candidate k-itemsets (Ck) from Lk-1
        candidate_itemsets = defaultdict(int)
        items = list(L1.keys())
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                new_candidate = tuple(sorted(set(items[i]).union(set(items[j]))))
                if len(new_candidate) == k:
                    # Count the frequency of the new candidate
                    candidate_itemsets[new_candidate] = sum(1 for transaction in transactions if set(new_candidate).issubset(transaction))

        # Filter candidates to get Lk
        L1 = {itemset: count for itemset, count in candidate_itemsets.items() if count >= min_support_count}
        frequent_itemsets.update(L1)

        k += 1

    # Step 6: Output all frequent itemsets
    for itemset, count in frequent_itemsets.items():
        print(f"Frequent Itemset: {itemset}, Support Count: {count}")

# Example usage
if __name__ == "__main__":
    # Adjust filename and minimal support level
    apriori('transactions.txt', 10)
