import pandas as pd
import numpy as np
from datetime import datetime

items = pd.read_csv("../ml-latest-small/movies.csv")

# Describe Table
print(items.describe())

# Number of Distinct Movies -> It's the same value as Describe Table
# This is a good validation to confirm that things are stable as items are added / subtracted daily
print("Number of distinct items: " + str(len(set(items["movieId"].to_numpy()))))

# Split out Title to Title and Year -> Used to analyze Movies Per Year

# [Minor] Validation on the following movie as multiple "()" found in the title value
# print(items[items['title'].str.contains('Cité des enfants perdus')])
# print(items[items['title'].str.contains('Nocturnal Animals')])
# print(items[items['title'].str.contains('Ready Player One')])

items['title_year'] = items.title.str.extract("\((\d{4})\)", expand=True)

items['title_year'] = pd.to_datetime(items['title_year'], format='%Y')
items['title_year'] = items['title_year'].dt.year # As there are some NaN years, resulting type will be float (decimals)
items.title = items.title.str[:-7]

# # Create Decade Buckets using title_year


# Genres Problem

genres_unique = pd.DataFrame(items.genres.str.split('|').tolist()).stack().unique()
genres_unique = pd.DataFrame(genres_unique, columns=['genre']) # Format into DataFrame to store later
items = items.join(items.genres.str.get_dummies().astype(int))
items.drop('genres', inplace=True, axis=1)

# [Minor] Validation that none of the Titles are Null (this should be 0) -> Use IMDB?
print ("Number of movies Null values: ", max(items.isnull().sum()))

# Genre Popularity / Frequency

# Plot Genre Frequency

# Links -> IMDB and TMBD_IDs


# Creating Additional Features
# print(items["movieId"].transform(lambda x: x + 1)) # to normalize ratings
