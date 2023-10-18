# ALS Model (Implicit) using sklearn
# Do To: ALS Model (Explicit) using sklearn

import pandas as pd
import numpy as np
from scipy.sparse.linalg import spsolve
from sklearn.preprocessing import MinMaxScaler

users_items = pd.read_csv("../data/links.csv")
print(users_items)
print(users_items.dtypes)