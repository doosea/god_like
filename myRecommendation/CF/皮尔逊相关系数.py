import pandas as pd

users = ["user1", "user2", "user3", "user4", "user5"]
items = ["item1", "item2", "item3", "item4", "item5"]

data = [
    [5, 3, 4, 4, None],
    [3, 1, 2, 3, 3],
    [4, 3, 4, 3, 5],
    [3, 3, 1, 5, 4],
    [1, 5, 5, 2, 1]
]

df = pd.DataFrame(data=data, columns=items, index=users)
print(df.corr())
print(df.T.corr())
