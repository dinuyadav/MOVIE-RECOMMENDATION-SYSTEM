import streamlit as st
import pandas as pd
import pickle
import requests
api_key ="8265bd1679663a7ea12ac168da84d2e8"
import gdown
import pickle

# URL of the file (Get from Google Drive)
file_url = "https://drive.google.com/file/d/1l3DJBmprEwLYcsg1snYkBiFltyrXtZYq/view?usp=sharing"

# Download the file
output = "model.pkl"
gdown.download(file_url, output, quiet=False)

# Load the pickle file
with open(output, 'rb') as f:
    model = pickle.load(f)

# Now you can use 'model' in your app


# Load Custom CSS
with open("stylee.css" ) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
# Injecting Custom CSS into Streamlit
#

def fetch_poster(movie_id):
    url = ("https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id))
    response = requests.get(url)
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path'] if 'poster_path' in data else ""

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    recommended_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    
    return recommended_movies, recommended_posters

#st.header('Movie Recommender System')
movies = pd.read_pickle(open('movie_list.pkl','rb'))

# Load data and similarity model
similarity = pd.read_pickle(open("similarity.pkl", "rb"))

st.title("Movie Recommendation System")
selected_movie = st.selectbox("Choose a movie", movies['title'].values)

if st.button("Recommend"):
    names, posters = recommend(selected_movie)
    cols = st.columns(5)
    for col, name, poster in zip(cols, names, posters):
        with col:
            st.image(poster, caption=name, use_container_width=True)
