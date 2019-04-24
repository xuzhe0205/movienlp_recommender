# Movie Reviews NLP & Recommender System

--------------------------------------------------------------------------

## Description:

Background:

* Movie Reviews NLP & Recommender System is a project aiming at making recommendation for users, consisting 2 parts: movie reviews NLP and KNN recommender system with visualization of a web app

### Dataset
Source: https://www.kaggle.com/dm4006/amazon-movie-reviews
Scale: Around 8 Million movie data
Dataset used in this project: subset of those 8 million data, 100K
Training set: 80%
Testing set: 20%

### Movie Reviews NLP

* Make use of data, specifically information like user reviews, conduct NLP by using fine grained and CNN algorithm (convolution neural network) to build and train a model that can take in large scale movie data and process natrual language from within, and finally return a table of 1 to 5 scale rating given by users to the movies, with 1  neg, 2: kind of neg, 3: netral, 4: kind of pos, 5: pos.

### Recommender System

* Make use of result from NLP part of the project, utilize KNN item-based collaborative filtering algorithm to build a k-Nearest Neighbor model that fit the data, result in a recommender system that is capable of taking in a query movie as input, and return a list of movies as recommendation.

### Web App

* Use Python and Flask framework to build a website for better workflow and result visualization for this project, as well as an emulation of user cases for the recommender system in this project

* User cases: 

1. Jump to `About` to check the introduction to this project and this system

2. Register

3. Login

4. Dashboard for browsing movies

5. Search for movies

6. Click on movie as the query movie, and recieve recommended movies in return


## Instruction

### To run models for NLP and Recommender System

* Open Jupyter Notebook from either Anaconda or Terminal

* Hit ```clear and run all``` from the kernal dropdown

### To run web app

* Open terminal and cd to folder `flask-app`

* Type ```python app.py```, and press enter to run



## Results & Comparison

### Movie Reviews NLP

* Accuracy: 72.5%

### Recommender System

* Movies recommended successfully match with the ranking of movie similarity for the query movie



