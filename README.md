
# Scalable Final Project

## Alexander Yonchev
## Fernando Vallecillos Ruiz

We discuss first the training and then the inference pipelines.
## Training Pipeline

### 01_json2df
Since the MPD is in JSON format and multiple slices, we need a script that reads all the slices and creates datasets for easy use later on.

Creates multiples dataframes:
- df_tracks_info: extra information about each track. E.g: artist, duration, album, tid, etc.
- df_tracks: information about which track belong to which playlist in which position
- df_playlists_info: information about each playlist. E.g: how many artists, edits, duration, name, how many tracks, etc.
- df_playlists_test and df_playlists_info: same as before but for the test set provided in the challenge.

It also creates a dictionary that links each track URI to a track ID.

### 02_buildChallengeSet
This script will build its own test set to create a more robust challenge with playlists from the original one that are missing a certain amount of tracks randomly or from the end.

- df_playlists_challenge: same as df_playlists but with the playlists chosen for the test set.
- df_tracks_challenge: same as df_tracks but with the tracks chosen for the test set.
- df_tracks_challenge_incomplete: same as df_tracks but with the modifications specified above.

### 03_buildTrainSet
This script creates the final training/test sets by substracting the previous sets from the original sets.

### 04_buildPlaylistSongMatrix
The dataframes created follow the template of df_tracks. This script creates new dataframes in which each row is a playlist with all the track IDs and their positions.

### 05_buildSongPlaylistMatrix
Creates extra dataframes in which each row is a track and specifies position and playlist ID it belongs to.

### 06_buildGiantMatrix
Creates the training playlist/song matrix. This matrix will have as many rows as playlists and as many columns as unique tracks. The songs belonging to a playlist will have a one in the corresponding place. Since it is a very large and sparse matrix, a sparse matrix is used.

### 07_buildGiantMatrix_truth
It will repeat the same process to create another matrix but this time it will be using the whole dataset instead of the training subset.

### 08_buildSimMatrix
This script builds a similarity matrix between playlists and between songs. This help to preprocess calculations later on.

### playlist_recommender
It test the model against the test set previously created. The results are:
R-Precision: 0.7607746294573476
NDCG: 0.768559893750165
Song Clicks: 0.0

## Inference Pipeline
We have made a Gradio app in HuggingFace to test the model:
[App](https://huggingface.co/spaces/nandovallec/spotify-recommender)

To this end we use the following scripts:
### fetchPlaylistTrackUris
Contains the neccesary functions to retrieve the URIs of the tracks given a playlist URL through the Spotify API.

### recommender
Contains the necessary functions to use the model given a list of URI.

### app
Main application that returns Spotify iframes according to the recommendations.

## Online Training Pipeline
Since music recommendation varies throughout the years, it is essential for the model to be able to retrain. For that reason the Inference pipeline has been modified to that goal.
Every time that an inference is made, the new list of URIs are saved in a dynamic dataset on Hugginface:
[Dataset 1](https://huggingface.co/datasets/nandovallec/df_ps_train_extra)
[Dataset 2](https://huggingface.co/datasets/nandovallec/giantMatrix_extra)
This processed data is added to the static dataset inmediately and therefore could be used in the next inference.
