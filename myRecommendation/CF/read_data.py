import pandas as pd
import numpy as np

dtype = {"userId": np.int32, "movieId": np.int32, "rating": np.float32}
df = pd.read_csv("../data/ml-latest-small/ratings.csv", dtype=dtype, usecols=range(3))
print(df)

rating_matrix = df.pivot_table(index=["userId"], columns=["movieId"], values=["rating"])
print(rating_matrix)

# print(rating_matrix.corr())
print(rating_matrix.T.corr())
