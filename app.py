import streamlit as st
import pandas as pd
from movie_recommender import get_recommendations, get_movie_details

# Load the data
df = pd.read_csv('movies.csv')

# Set page config
st.set_page_config(page_title="Movie Recommender System", layout="wide", initial_sidebar_state="expanded")

# Custom CSS to improve the look and feel
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6
    }
    .sidebar .sidebar-content {
        background: #262730
    }
    .Widget>label {
        color: #262730;
        font-family: sans-serif;
    }
    .stButton>button {
        color: #4e8cff;
        background-color: #262730;
        border-radius: 5px;
    }
    .stTextInput>div>div>input {
        color: #4e8cff;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.title("🎬 Movie Recommender System")
st.markdown("Discover new movies based on your preferences!")

# Sidebar for user input
with st.sidebar:
    st.header("📌 Movie Input")
    selected_movie = st.text_input("Enter a movie title", "")
    st.markdown("---")
    st.info("This system uses content-based filtering to recommend movies similar to your selection.")
    st.text("Created by Sameer")

# Main content
col1, col2 = st.columns([1, 2])

with col1:
    st.header("🎥 Selected Movie")
    if selected_movie:
        matching_movies = df[df['title'].str.contains(selected_movie, case=False, na=False)]
        if not matching_movies.empty:
            exact_match = matching_movies[matching_movies['title'].str.lower() == selected_movie.lower()]
            if not exact_match.empty:
                movie_details = get_movie_details(exact_match.iloc[0]['title'])
            else:
                movie_details = get_movie_details(matching_movies.iloc[0]['title'])
            
            st.subheader(movie_details['title'])
            st.write(f"**Genres:** {movie_details['genres']}")
            st.write(f"**Release Date:** {movie_details['release_date']}")
            st.write(f"**Average Vote:** {movie_details['vote_average']}/10")
            st.write("**Overview:**")
            st.write(movie_details['overview'])
        else:
            st.warning("No matching movie found. Please try another title.")

with col2:
    st.header("🍿 Recommendations")
    if st.button("Get Recommendations", key="rec_button"):
        if selected_movie and not matching_movies.empty:
            with st.spinner("Finding similar movies..."):
                movie_id = matching_movies.iloc[0]['id']
                recommendations = get_recommendations(movie_id)
                
                for i, movie in enumerate(recommendations, 1):
                    with st.expander(f"{i}. {movie}"):
                        rec_details = get_movie_details(movie)
                        st.write(f"**Genres:** {rec_details['genres']}")
                        st.write(f"**Release Date:** {rec_details['release_date']}")
                        st.write(f"**Average Vote:** {rec_details['vote_average']}/10")
                        st.write("**Overview:**")
                        st.write(rec_details['overview'])
        elif selected_movie:
            st.warning("Please enter a valid movie title to get recommendations.")
        else:
            st.warning("Please enter a movie title to get recommendations.")

# Add a footer
st.markdown("---")
st.markdown("Made by Sameer")
