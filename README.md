# Music Recommender

Music recommender with a knowledge base (the Music Recommendation System dataset from Kaggle)


<img src="images/main_screen.png" alt="main_screen" width="500"/>

## Features

- **Interactive Filtering**
  - The system can filter songs by asking the user a series of questions.
  - Based on the user's responses, it narrows down the dataset to match user preferences.

- **Song Guessing with Decision Trees**
  - Trains a Decision Tree Classifier on the dataset.
  - Tests the user's ability to identify a song by navigating the optimal decision path.

- **Genre-Based Recommendation**
  - Applies K-Means clustering (unsupervised learning) to group the dataset into 5 genres:
    - EDM
    - Rock
    - Pop
    - Jazz
    - Classical
  - Recommends songs by computing Euclidean distances from a given song to others in the same cluster.