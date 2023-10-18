import pandas as pd
from datetime import datetime

items = pd.read_csv("../data/movies.csv")
print(items)
print(items.dtypes)

# Describe Table
print(items.describe())

# Number of Distinct Movies -> It's the same value as Describe Table
# This is a good validation to confirm that things are stable as items are added / subtracted daily
print("Number of distinct items: " + str(len(set(items["movieId"].to_numpy()))))

# Split out Title to Title and Year -> Used to analyze Movies Per Year
items['title_year'] = items['title'].str.replace(')','') \
                    .str.split('(') \
                    .str[1]

items['title'] = items['title'].str.replace(')','') \
                    .str.split('(') \
                    .str[0][:-1] 

# Create Categorical Buckets per Decade
# Ran into an issue with movie = Cité des enfants perdus, La
    # Search for the movie
    # Figure out how I need to resplit


def convert(dt):
    try:
        return datetime.strptime(dt, '%d/%m/%Y').strftime('%d/%m/%Y')
    except ValueError:
        return datetime.strptime(dt, '%m/%d/%Y').strftime('%d/%m/%Y')

items['title_date'] = '01/01/' + items['title_year'].astype(str)
items['title_date'] = items['title_date'].apply(convert)
print(items)
print(items.dtypes)


# items['decade'] = items['title_year'].

# Genres Problem

# Genre Popularity / Frequency

# Plot Genre Frequency

# Links -> IMDB and TMBD_IDs


# Creating Additional Features
# print(items["movieId"].transform(lambda x: x + 1)) # to normalize ratings
