# movielens_lessons: Models

# Prereq
Before replicating any of the models, you must complete the [Prereqs](https://github.com/sambk17/movielens_lessons#prereqs) and download the MovieLens Latest Dataset (100k).  Doing so gives you access to the  User x Item records


# Model Frameworks

* Pandas / Sklearn
* PySpark (MLlib)
* Tensorflow
* PyTorch

# How To Run This?
If you have the downloaded data in your repo, it is as simple as running:
```
python {model}_{framework}.py
```
So far supported:
* als_sklearn.py
* als_pyspark.py

Objectives:
* Pass in parameters for train, test, date_range
* Output model artifact
* Move on to Feature Engineering w/ Feast