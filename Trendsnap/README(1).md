
# TrendSnap – AI-Based Hashtag Recommender Using NLP and Machine Learning

## 📖 Introduction

TrendSnap is an intelligent hashtag recommendation system that uses Natural Language Processing (NLP) and Machine Learning techniques to generate relevant hashtags from user captions. The system understands the semantic meaning of a caption instead of relying on simple keyword matching. By leveraging BERT embeddings, cosine similarity, and Linear Regression, TrendSnap recommends hashtags that improve the visibility and reach of social media posts.

The application also integrates with the Twitter API to collect recent tweets related to the caption and extract trending hashtags. If no hashtags are found, the application automatically uses a predefined dataset of popular hashtags to ensure uninterrupted recommendations.

---

# Objectives

- Develop an intelligent hashtag recommendation system.
- Improve social media post discoverability.
- Analyze captions using Natural Language Processing.
- Recommend semantically relevant hashtags.
- Compare hashtags using cosine similarity.
- Predict similarity scores using Linear Regression.
- Visualize recommendation results.

---

# Key Features

- User-friendly Streamlit interface
- Caption preprocessing using spaCy
- Semantic text understanding using BERT
- Twitter API integration for live hashtag extraction
- Automatic fallback hashtag recommendations
- Cosine similarity-based ranking
- Machine Learning prediction using Linear Regression
- Interactive charts using Matplotlib and Seaborn
- Regression performance evaluation using R² Score and Mean Squared Error

---

# Technology Stack

| Category | Technologies |
|----------|--------------|
| Programming Language | Python |
| Frontend | Streamlit |
| NLP | spaCy, BERT (Transformers) |
| Deep Learning | PyTorch |
| Machine Learning | Scikit-learn (Linear Regression) |
| API | Twitter API v2 (Tweepy) |
| Data Processing | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn |
| Environment | python-dotenv |

---

# Project Architecture

User Caption
      ↓
Text Preprocessing (spaCy)
      ↓
BERT Embedding Generation
      ↓
Twitter API Tweet Collection
      ↓
Hashtag Extraction
      ↓
Cosine Similarity Calculation
      ↓
Top Hashtag Ranking
      ↓
Linear Regression Prediction
      ↓
Visualization & Performance Metrics

---

# Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/TrendSnap.git
cd TrendSnap
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Install spaCy Model

```bash
python -m spacy download en_core_web_sm
```

## Configure Twitter API

Create a `.env` file.

```text
TWITTER_BEARER_TOKEN=YOUR_TWITTER_BEARER_TOKEN
```

## Run

```bash
streamlit run trendsnap2.py
```

---

# Workflow

1. User enters a caption.
2. Caption is cleaned using spaCy.
3. BERT generates semantic embeddings.
4. Twitter API fetches recent tweets.
5. Hashtags are extracted.
6. Cosine similarity scores are calculated.
7. Top hashtags are ranked.
8. Linear Regression predicts similarity scores.
9. Charts and metrics are displayed.

---

# Machine Learning

## Model Used

Linear Regression predicts hashtag similarity scores using:

- BERT embedding vectors
- Hashtag length

### Evaluation Metrics

- R² Score
- Mean Squared Error (MSE)

---

# Output

The application displays:

- Top recommended hashtags
- Similarity score table
- Bar chart
- Similarity score distribution
- Sample tweets
- Regression scatter plot
- R² Score
- Mean Squared Error

---

# Future Scope

- Instagram and Threads API integration
- Multiple Machine Learning model comparison
- User authentication
- Database storage
- Real-time trending hashtag analysis
- Multilingual caption support
- Engagement prediction
- Mobile application deployment

---

# Advantages

- Intelligent semantic recommendations
- Real-time trending hashtag extraction
- Easy-to-use interface
- Fast prediction
- Interactive analytics
- Better social media reach

---

# Author

**Mohammed Aashik**

MCA Student  
SRM Institute of Science and Technology

---

# License

This project is developed for academic and educational purposes.
