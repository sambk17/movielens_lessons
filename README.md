# movielens_lessons
Hello World :wave:!  This repository encompasses some of the valuable lessons I learned with Recommender Systems @ HBO/HBO Max/Warner Bros. Discovery.  Since I worked A LOT with user-item interactions, it is most fitting that everything is  performed using public data only (aka MovieLens).  Since my hope is someone will clone this repo, I will stick to the latest dataset of 100K.

# Prereqs
* Download MovieLens Latest Dataset [ml-latests-small.zip](https://grouplens.org/datasets/movielens/)
  * Note: This is the 100k small dataset: 100,000 ratings and 3,600 tag applications applied to 9,000 movies by 600 users. Last updated 9/2018.
* [Optional] Create a folder in the root of this repo called `data/` (e.g. `movielens_lessons/data/`)

# Library Dependencies / Installations
* Create a virtual environment: https://docs.python.org/3/library/venv.html
* After activating your virtual environment, `pip install -r requirements.txt`

# Exploratory Data Analysis
* `eda/` folder to be created to explore information about the user x item relationship

# Models - Implicit vs Explicit
* ALS
* EASE
* XGBoost

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
