import streamlit as st
import pickle
import pandas as pd
import requests

@st.cache
def fetch_poster(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
    data=response.json()

    return "https://image.tmdb.org/t/p/w500" + data['poster_path']


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])

    recommend_movies=[]
    recommend_movies_posters=[]
    for i in distances[0:6]:
        movie_id=movies.iloc[i[0]].movie_id
        recommend_movies.append(movies.iloc[i[0]].title)
        recommend_movies_posters.append(fetch_poster(movie_id))

    return recommend_movies,recommend_movies_posters


movies_dict=pickle.load(open('movie1_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)

similarity=pickle.load(open('similarity1.pkl','rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox('Select a Movie',movies['title'].values)

if st.button('search'):

    names,posters=recommend(selected_movie_name)

    c1,c2,c3=st.beta_columns(3)
    with c1:
        st.write(names[0])
        st.image(posters[0])


    st.write('Recommended Movies')
    col1, col2, col3, col4, col5= st.beta_columns(5)
    col=[col1,col2,col3,col4,col5]
    for i in range(1,6):
        with col[i-1]:
            st.text(names[i])
            st.image(posters[i])



