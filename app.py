import streamlit as st
import pandas as pd
import pickle
import requests

# ----------------------------------------------------
# 1. PAGE CONFIGURATION & THEME INJECTION
# ----------------------------------------------------
st.set_page_config(
    page_title="CineMatch | Movie Recommendations",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for a clean, cinematic dark UI/UX with modern card hover effects
st.markdown("""
    <style>
    /* Main background and font styling */
    .main {
        background-color: #0e1117;
        color: #ffffff;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    /* Header Banner Styling */
    .hero-container {
        text-align: center;
        padding: 2rem 0rem 3rem 0rem;
        background: linear-gradient(180deg, rgba(229,9,20,0.15) 0%, rgba(14,17,23,0) 100%);
        border-radius: 12px;
        margin-bottom: 2rem;
    }
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        color: #E50914;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }
    .hero-subtitle {
        font-size: 1.2rem;
        color: #a0aec0;
        font-weight: 400;
    }

    /* Custom Movie Card Layout */
    .movie-card {
        background-color: #1a1f2c;
        border-radius: 10px;
        padding: 0px;
        margin-bottom: 20px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border: 1px solid #2d3748;
        overflow: hidden;
        height: 100%;
    }
    .movie-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(229, 9, 20, 0.2);
        border-color: #E50914;
    }
    .movie-title {
        font-size: 1.05rem;
        font-weight: 700;
        padding: 12px 10px 5px 10px;
        color: #ffffff;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .movie-meta {
        font-size: 0.85rem;
        color: #e50914;
        padding: 0px 10px 12px 10px;
        font-weight: 600;
    }
    
    /* Customizing Streamlit interactive elements */
    div.stButton > button:first-child {
        background-color: #E50914;
        color: white;
        font-weight: 700;
        border-radius: 6px;
        border: none;
        padding: 0.6rem 2rem;
        transition: background-color 0.2s ease;
        width: 100%;
    }
    div.stButton > button:first-child:hover {
        background-color: #b80710;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# ----------------------------------------------------
# 2. DATA & MODEL LOADING (CACHED)
# ----------------------------------------------------
@st.cache_resource
def load_model_data():
    
    try:
        movies_df = pickle.load(open("movies.pkl", "rb")) 
        # Placeholder for your similarity matrix (cosine_sim)
        similarity_matrix = pickle.load(open("similarity.pkl", "rb"))
        
        return movies_df, similarity_matrix
    except Exception as e:
        st.error(f"Error loading model artifacts: {e}")
        return None, None

movies_df, similarity_matrix = load_model_data()

# ----------------------------------------------------
# 3. HELPER FUNCTIONS
# ----------------------------------------------------
# Add your API key here (in production, use st.secrets!)
TMDB_API_KEY = st.secrets["TMDB_API_KEY"]

@st.cache_data(show_spinner=False)
def get_movie_poster(movie_title):
    """
    Fetches the actual poster image URL using the TMDB API.
    Falls back to a placeholder if the API fails or no poster exists.
    """
    try:
        # 1. Search the TMDB database for the movie title
        search_url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_title}"
        response = requests.get(search_url)
        data = response.json()
        
        # 2. Extract the poster_path from the first search result
        if data.get('results'):
            poster_path = data['results'][0].get('poster_path')
            
            if poster_path:
                # 3. Combine the base image URL with the specific poster path
                return f"https://image.tmdb.org/t/p/w500{poster_path}"
                
        # Fallback if the movie is found but has no poster uploaded
        return "https://images.unsplash.com/photo-1536440136628-849c177e76a1?q=80&w=300&auto=format&fit=crop"
        
    except Exception as e:
        # Fallback if the API is down or rate-limited
        return "https://images.unsplash.com/photo-1536440136628-849c177e76a1?q=80&w=300&auto=format&fit=crop"

def get_recommendations(movie_name, df, sim_matrix):
    # 1. Get the index of the movie that matches the title
     idx = df[df['title'] == movie_name].index[0]
    
    # 2. Get pairwise similarity scores and sort them (highest similarity first)
     distances = sorted(list(enumerate(sim_matrix[idx])), reverse=True, key=lambda x: x[1])
    
    # 3. Extract top 5 movie indices (excluding the first one, which is the movie itself)
     movie_indices = [i[0] for i in distances[1:6]]
    
    # 4. Fetch the movie records and convert to list of dictionaries
     recommendations = df.iloc[movie_indices].to_dict(orient='records')
    
     return recommendations


# ----------------------------------------------------
# 4. USER INTERFACE LAYOUT
# ----------------------------------------------------

# Hero Header section
st.markdown("""
    <div class="hero-container">
        <div class="hero-title">🎬 CineMatch</div>
        <div class="hero-subtitle">Find your next favorite film using intelligence, not guesswork.</div>
    </div>
""", unsafe_allow_html=True)

# Search/Selection Controls row
col_space1, col_input, col_btn, col_space2 = st.columns([1, 4, 1.5, 1])

with col_input:
    selected_movie = st.selectbox(
        "Type or select a movie you enjoy:",
        options=movies_df['title'].values,
        label_visibility="collapsed",
        index=0
    )

with col_btn:
    trigger_recommend = st.button("Get Recommendations")

st.markdown("---")

# ----------------------------------------------------
# 5. EXECUTION & RESULTS PRESENTATION GRID
# ----------------------------------------------------
if trigger_recommend:
    with st.spinner("Analyzing cinematic patterns..."):
        recs = get_recommendations(selected_movie, movies_df, similarity_matrix)
        
        if recs:
            st.markdown("### 🍿 Handpicked For You")
            
            # Create a symmetric 5-column grid layout for the recommendations
            grid_cols = st.columns(5)
            
            for idx, movie in enumerate(recs):
                poster_url = get_movie_poster(movie['title'])
                
                with grid_cols[idx]:
                    # Render the beautiful card using targeted HTML injection
                    st.markdown(f"""
                        <div class="movie-card">
                            <img src="{poster_url}" style="width:100%; height:240px; object-fit:cover; display:block;" alt="{movie['title']}">
                            <div class="movie-title" title="{movie['title']}">{movie['title']}</div>
                            <div class="movie-meta">{movie.get('genres', '')}</div> 
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("No recommendations found. Try adjusting your input criteria.")
else:
    # Neutral, welcoming landing state when the app is initialized
    st.info("💡 Select a movie from the dropdown above and hit 'Get Recommendations' to see the grid fill up.")