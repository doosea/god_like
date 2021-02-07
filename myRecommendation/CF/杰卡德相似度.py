from sklearn.metrics import jaccard_score
import pandas as pd

users = ["user1", "user2", "user3", "user4", "user5"]
items = ["item1", "item2", "item3", "item4", "item5"]

data = [
    [1, 0, 1, 1, 0],
    [1, 0, 0, 1, 1],
    [1, 0, 1, 0, 0],
    [0, 1, 0, 1, 1],
    [1, 1, 1, 0, 1]
]

df = pd.DataFrame(data=data, columns=items, index=users)
print(jaccard_score(df['item1'], df['item2']))
