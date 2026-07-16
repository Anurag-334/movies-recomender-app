# 🎬 CineMatch: Content-Based Movie Recommendation System

A sleek, content-based movie recommendation system built using **Natural Language Processing (NLP)** and **Machine Learning**. The project features a data processing pipeline that merges movie metadata, extracts key features, uses a Bag-of-Words text vectorization approach, and calculates geometric distances to recommend contextually similar films.

Used TMDB 5000 dataset: https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata?select=tmdb_5000_movies.csv

A fully working version is wrapped in a highly responsive, cinematic custom-themed **Streamlit** user interface featuring live dynamic poster streaming via the **TMDB API**.

---

## 🚀 System Architecture & Workflow

The recommendation model relies on a clean, end-to-end data processing workflow:

```text
[tmdb_5000_movies.csv] + [tmdb_5000_credits.csv] 
                        │
                        ▼ (Inner Merge on Title)
               [Combined Dataset]
                        │
                        ▼ (Feature Selection: id, title, overview, genres, keywords, cast, crew)
             [Raw Structural Columns]
                        │
                        ▼ (AST Parsing & Space Collapse)
                 [Cleaned Tokens]
                        │
                        ▼ (NLTK Porter Stemming & Lowercase)
                  [Merged 'tags']
                        │
                        ▼ (CountVectorizer - Max 5000 Features)
                 [Text Vectorization]
                        │
                        ▼ (Cosine Similarity Matrix)
             [Content Filtering Model]

```

---

## 🧠 Model Technical Implementation

### 1. Data Merging & Feature Engineering

* **Dataset Fusion:** The pipeline ingests raw `tmdb_5000_movies.csv` and `tmdb_5000_credits.csv` tables, applying an inner merge on the `'title'` string.


* **Dimensional Reduction:** Drops irrelevant statistical rows and selects key context features: `movie_id`, `title`, `overview`, `genres`, `keywords`, `cast`, and `crew`.


* **Abstract Syntax Tree (AST) Extraction:** Evaluates stringified JSON columns to extract functional names (e.g., retrieving individual genre descriptors, mapping keywords, locating the top three structural billing cast members, and picking out the **Director** from the crew dictionary).



### 2. Natural Language Processing (NLP)

* **Space Collapse:** Spaces are intentionally removed from string entities (e.g., changing `"Christopher Nolan"` to `"ChristopherNolan"`) to prevent the model's text vectorizer from separating unique entity phrases.


* **Tag Compounding:** Text blocks are grouped together into a master string element labeled `'tags'`.


* **Porter Stemming Algorithm:** Words inside the combined blocks are reduced to their root forms using the `nltk.stem.porter` package (e.g., converting `"activities"`, `"activity"`, or `"action"` down to common stems) to boost vocabulary matching rates across movies.



### 3. Vectorization & Similarity Computations

* **Bag of Words (BoW):** The system relies on a `CountVectorizer` initialized to capture the top **5,000** non-stop-word structural features across the corpus.


* **Cosine Similarity:** Instead of computing standard Euclidean distance (which fails on high-dimensional text matrices), the pipeline computes spatial cosine similarity scores. It maps directional angle variations between the 5,000-dimensional vectors via:



$$\text{Similarity}(A, B) = \frac{A \cdot B}{\Vert{}A\Vert{} \Vert{}B\Vert{}}$$

---

## 🛠️ Project File Layout

```text
.
├── .streamlit/
│   └── secrets.toml         # Secure API keys for external streaming services
├── data/
│   ├── tmdb_5000_credits.csv # Original production crew credits dataset
│   └── tmdb_5000_movies.csv  # Original technical movie summary metadata
├── notebook/
│   └── Movie_Recommendation.ipynb # Model design, engineering, and training ledger
├── app.py                   # High-fidelity custom dark-themed UI script
├── requirements.txt         # Global package version guidelines
├── movies.pkl               # Serialized structural dataframe index mapping
└── similarity.pkl           # Trained high-dimensional cosine similarity matrix

```

---

## 💻 Quick Start Installation & Execution

### 1. Replicate the Virtual Environment

Ensure Python 3.10+ is initialized, open your terminal inside the root directory, and execute:

```bash
# Generate the isolated environment
python -m venv .venv

# Activate the local workspace environment (Windows)
.venv\Scripts\activate

# Activate the local workspace environment (Mac/Linux)
source .venv/bin/activate

# Install essential package components
pip install -r requirements.txt

```

### 2. Local App Server Deployment

Run the Streamlit frontend locally to verify database configurations and view the visual layout:

```bash
streamlit run app.py

```

---

## ⚙️ App Configurations & Secrets Management

To run the app with live movie posters without hardcoding sensitive access keys, your local `.streamlit/secrets.toml` must align with the deployment platform dashboard inputs:

```toml
# Place inside your local .streamlit/secrets.toml file
TMDB_API_KEY = "your_secret_32_character_developer_key"

```

---

## 📊 Sample Inference Evaluation Output

When passing a query through the recommendation logic, the system filters out the user's input and pulls the top five closest vector records:

```python
# Execution statement inside the model logic
recommend("Batman Begins")

```

**System Engine Output Matrix:**

1. `The Dark Knight`

2. `Batman`

3. `Batman`

4. `The Dark Knight Rises`

5. `10th & Wolf`
