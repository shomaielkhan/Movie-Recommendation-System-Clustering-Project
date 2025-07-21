import streamlit as st
import random
import pandas as pd
import numpy as np
from streamlit_lottie import st_lottie
import json

#lottie_json=json.load(open("animation.json"))
#st_lottie(lottie_json, height=200)


df_movies=pd.read_csv("clustered_movies.csv")

def recommend_movie(movie_name: str):
    #movie name to lowrcase for case insensitive matching
    movie_name=movie_name[0].lower()
    #new column 'name' to store titles values for comparison (lower case)
    df_movies['name']= df_movies['name'].str.lower()
    #find the movie which matches the inpute name
    movie=df_movies[df_movies['name'].str.contains(movie_name, na=False)]

    if not movie.empty:
        #Get the cluster label
        clusters=movie['dbscan_clusters'].values[0]
        #get all the movies of the same clusters
        cluster_movies=df_movies[df_movies['dbscan_clusters']==clusters]
        #select only 5 movies in the clusters
        if len(cluster_movies) >= 5:
            #randomly select 5
            recommended_movies =random.sample(list(cluster_movies['name']), 5)
        else:
            #if fewer then 5, return all the movies in the cluster
            recommended_movies=list(cluster_movies['name'])
        #print the recommended movies
        return recommended_movies
    else:
        print("Movie not found in the Database.")


st.set_page_config(layout="wide")
col1,col2=st.columns([4,4])
col1.header('Movie Recommendation System')
col2.image("Dashboard/logo2.png",width=100)

st.markdown("-----------------------------------------")
with st.container():
    st.subheader("Supported Databases")
    st.write("Netflix TV Shows and Movies")
    st.write("HBOMax TV Shows and Movies")
    st.write("Amazon Prime TV Shows and Movies")
    st.markdown("-----------------------------------------")

tab1, tab2 = st.tabs(["Search", "About"])

with tab1:

    movie_name=df_movies['name'].values
    movie_names=st.selectbox("Search for a movie you like",options=movie_name)
with tab2:
    st.markdown("This app recommend movies using DBSCAN Clustering...")

if st.button("Recommend"):
    st.write("---We recommend you these movies---")
    recommendation=recommend_movie(movie_name)
    st.dataframe(recommendation)



st.markdown("---")
st.markdown('@2025 | Built by Shomaiel Khan | email: shomaielkhan364@gmail.com')