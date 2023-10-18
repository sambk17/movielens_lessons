# movielens_lessons
Hello World :wave:!  This repository encompasses many of the valuable lessons I learned with Recommender Systems while at HBO/HBO Max/Warner Bros. Discovery.  Since I worked A LOT with user-item interactions over the years, it is most fitting that everything here is performed using public data only (aka MovieLens dataset).  Since my hope is to help others learn for educational or academic purposes, I will stick to the smallest and latest dataset (100K).

# Prereqs
* Download MovieLens Latest Dataset [ml-latests-small.zip](https://grouplens.org/datasets/movielens/)
  * Note: This is the 100k small dataset: 100,000 ratings and 3,600 tag applications applied to 9,000 movies by 600 users. Last updated 9/2018.
* [Optional] Create a folder in the root of this repo called `data/` (e.g. `movielens_lessons/data/`)
* [Optional] Download [IMDB Non-Commercial Datasets](https://developer.imdb.com/non-commercial-datasets/) to further enrich the Movies (items): [Link](https://datasets.imdbws.com/).  Save the following files under `data/` folder:
  * title.basics.tsv.gz (171MB)
  * title.ratings.tsv.gz (7MB)

# Library Dependencies / Installations
* Create a virtual environment: https://docs.python.org/3/library/venv.html
* After activating your virtual environment, `pip install -r requirements.txt`

# Exploratory Data Analysis
* `eda/` folder to be created to explore information about the user x item relationship
* I will include a README to recount some valuable lessons learned while working with Feature Engineering of this dataset (but with real data).  
* If you have an interesting Feature Engineering problem that's applicable (e.g. you experienced with your professional work) and should be included in this section, please contact me directly :smile:

# Models - Implicit vs Explicit
* I will go into detail about computing predictions using either implicit (the interaction only) or explicit (ratings)
* Models I'm knowledgeable with:
  * ALS
  * Matrix Factorization (LightFM)
  * Encoders (EASE)
  * XGBoost
  * [Future] Neural Networks (I don't think they do much)

# Model Frameworks
* Pandas / Sklearn
* PySpark (MLlib)
* Tensorflow
* PyTorch

# Offline Evaluation
* How to Compute Accurary
* Gini Coefficient
* Understanding Novelty

## To-Dos
* Jupyter Notebook -> How to Train a Model?  ALS, LightFM, Ease and XGBoost
* Jupyter Notebook -> How to Evaluate a Model?
* How to make a Model Prediction?


## References
* IMDB Preprocessing: https://github.com/jennyzhang0215/MovieLens-IMDB/tree/master
* EDA Visualizations: https://www.kaggle.com/code/cesarcf1977/movielens-data-analysis-beginner-s-first/notebook
