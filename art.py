import streamlit as st
import pickle
import pandas as pd
import random
import requests

def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://images.pexels.com/photos/1763075/pexels-photo-1763075.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url()
def recommend(song):
    song_index = songs[songs['track'] == song].index[0]
    distances = similarity[song_index]
    songs_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:16]

    random.shuffle(songs_list)
    recommended_songs = []
    for i in songs_list:
        recommended_songs.append(songs.iloc[i[0]])
    return recommended_songs

def get_album_art(song):
    url = f"https://api.spotify.com/v1/search?q={song['track']} {song['spotify_id']}&type=track&limit=1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'tracks' in data and 'items' in data['tracks'] and len(data['tracks']['items']) > 0:
            album_art_url = data['tracks']['items'][0]['album']['images'][0]['url']
            return album_art_url
    return None

song_dict2 = pickle.load(open('song_dict.pkl', 'rb'))
songs = pd.DataFrame(song_dict2)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title("Music Recommendation System")

selected_song_name = st.selectbox("Select the song you wanna use as a reference", songs['track'].values)

if st.button('Recommend'):
    selected_song = songs[songs['track'] == selected_song_name].iloc[0]
    recommended_songs = recommend(selected_song_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    for song in recommended_songs[:5]:
        with col1:
            album_art_url = get_album_art(song)
            if album_art_url:
                st.image(album_art_url, use_column_width=True)
            st.text(song['track'])

        recommended_songs = recommended_songs[1:]

