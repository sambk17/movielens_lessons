import pandas as pd
import numpy as np
from datetime import datetime

items = pd.read_csv("../data/movies.csv")

# Describe Table
print(items.describe())

# Number of Distinct Movies -> It's the same value as Describe Table
# This is a good validation to confirm that things are stable as items are added / subtracted daily
print("Number of distinct items: " + str(len(set(items["movieId"].to_numpy()))))

# Split out Title to Title and Year -> Used to analyze Movies Per Year

# [Minor] Validation on the following movie as multiple "()" found in the title value
# print(items[items['title'].str.contains('Cité des enfants perdus')])
print(items[items['title'].str.contains('Nocturnal Animals')])
print(items[items['title'].str.contains('Ready Player One')])

items['title_year'] = items['title'].str.replace(')','') \
                    .str.split('(') \
                    .str[-1]

items['title'] = items['title'].str.replace(')','') \
                    .str.split('(') \
                    .str[0]


# [Minor] Validation that none of the Titles are Null (this should be 0)
# print(np.sum(items['title'].isnull().to_numpy()))
# print(items[items['title'].str.contains('City of Lost Children')])

# # Create Categorical Buckets per Decade

print(items['title_year'].sort_values())

# def convert(dt):
#     try:
#         return datetime.strptime(dt, '%d/%m/%Y').strftime('%d/%m/%Y')
#     except ValueError:
#         return datetime.strptime(dt, '%m/%d/%Y').strftime('%d/%m/%Y')

# items['title_date'] = '01/01/' + items['title_year'].astype(str)
# items['title_date'] = items['title_date'].apply(convert)
# print(items)
# print(items.dtypes)


# items['decade'] = items['title_year'].

# Genres Problem

# Genre Popularity / Frequency

# Plot Genre Frequency

# Links -> IMDB and TMBD_IDs


# Creating Additional Features
# print(items["movieId"].transform(lambda x: x + 1)) # to normalize ratings
