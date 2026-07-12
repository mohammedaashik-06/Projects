import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import re
import spacy
import torch
import numpy as np
import tweepy
from dotenv import load_dotenv
import os
from transformers import BertTokenizer, BertModel
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

if not TWITTER_BEARER_TOKEN:
    st.error("Twitter Bearer Token not found. Please set TWITTER_BEARER_TOKEN in your .env file.")
    st.stop()

client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN)
nlp = spacy.load("en_core_web_sm")
bert_tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
bert_model = BertModel.from_pretrained("bert-base-uncased")


def preprocess_caption(text):
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return " ".join(tokens)

def get_bert_embedding(text):
    inputs = bert_tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = bert_model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).numpy()

def fetch_hashtags_from_twitter(query, max_results=30):
    try:
        keywords = preprocess_caption(query)
        search_query = keywords + " -is:retweet lang:en"
        tweets = client.search_recent_tweets(query=search_query, max_results=max_results, tweet_fields=["text"])
        hashtags = []
        texts = []
        if tweets.data:
            for tweet in tweets.data:
                tags = re.findall(r"#\w+", tweet.text)
                hashtags.extend(tags)
                if tags:
                    texts.append(tweet.text)
        return list(set(hashtags)), texts
    except Exception as e:
        st.error(f"Twitter API Error: {e}")
        return [], []

def rank_hashtags(caption, hashtag_list, top_n=5, min_score=0.3):
    if not hashtag_list:
        return []
    processed_caption = preprocess_caption(caption)
    caption_embedding = get_bert_embedding(processed_caption)
    hashtag_embeddings = np.vstack([get_bert_embedding(tag) for tag in hashtag_list])
    similarities = cosine_similarity(caption_embedding, hashtag_embeddings)[0]
    ranked = sorted(zip(hashtag_list, similarities), key=lambda x: x[1], reverse=True)
    filtered = [item for item in ranked if item[1] >= min_score]
    return filtered[:top_n]

def get_embedding_vector(tag):
    return get_bert_embedding(tag).flatten()

def train_regression_model(df):
    if df.empty or "Hashtag" not in df.columns or df["Hashtag"].dropna().empty:
        raise ValueError("No valid hashtags available for training.")

    df["Length"] = df["Hashtag"].apply(len)

    hashtag_list = df["Hashtag"].dropna().tolist()
    if not hashtag_list:
        raise ValueError("No hashtags found to generate embeddings.")

    embedding_features = np.vstack([get_embedding_vector(tag) for tag in hashtag_list])
    X = np.hstack((df["Length"].values.reshape(-1, 1), embedding_features))
    y = df["Similarity Score"].values

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    reg = LinearRegression()
    reg.fit(X_train, y_train)
    y_pred = reg.predict(X_test)

    return reg, X_test, y_test, y_pred

st.set_page_config(page_title="TrendSnap ML Regression", layout="wide")
st.title("TrendSnap Regression – Predicting Hashtag Similarity Score")

caption = st.text_input("Enter a caption for analysis", value="Exploring the nature")

if st.button("Analyze & Train Regression"):
    with st.spinner("Fetching tweets, analyzing & training model..."):
        hashtags, tweet_texts = fetch_hashtags_from_twitter(caption)
        if not hashtags:
            st.warning("No hashtags were found for the given caption. Trying fallback suggestions...")
            hashtags = [
                "#travel", "#wanderlust", "#nature", "#adventure", "#vacation", "#travelgram", "#explore", "#beachlife", "#hiking", "#sunset",
                "#foodie", "#foodstagram", "#yummy", "#homecooking", "#coffee", "#coffeetime", "#brunch", "#dessert", "#foodphotography",
                "#fashion", "#style", "#ootd", "#makeup", "#skincare", "#streetstyle", "#hairstyle", "#fashionblogger", "#beautytips",
                "#coding", "#programming", "#developer", "#webdev", "#tech", "#ai", "#machinelearning", "#datascience", "#python", "#startup",
                "#motivation", "#selflove", "#growth", "#goals", "#mindset", "#positivity", "#mentalhealth", "#focus", "#discipline",
                "#fitness", "#workout", "#fitlife", "#gym", "#healthylifestyle", "#yoga", "#wellness", "#running", "#nutrition", "#bodygoals",
                "#gaming", "#gamer", "#streaming", "#videogames", "#twitch", "#esports", "#anime", "#memes", "#funny", "#memeoftheday",
                "#photography", "#photooftheday", "#art", "#illustration", "#creative", "#aesthetic", "#design", "#artist", "#digitalart",
                "#studygram", "#productivity", "#learning", "#studymotivation", "#notetaking", "#booklover", "#reading", "#edtech"
            ]
            top_ranked = rank_hashtags(caption, hashtags, top_n=10, min_score=0.1)
        else:
            top_ranked = rank_hashtags(caption, hashtags, top_n=10, min_score=0.3)

        if not top_ranked:
            st.warning("No meaningful similarity scores could be computed.")
        else:
            df = pd.DataFrame(top_ranked, columns=["Hashtag", "Similarity Score"])
            for tag, score in top_ranked:
                st.write(f"Hashtag: {tag}, Similarity Score: {score:.4f}")

            st.subheader("🔍 Top Hashtags Similarity Scores")
            fig1, ax1 = plt.subplots()
            sns.barplot(x="Similarity Score", y="Hashtag", data=df, palette="viridis", ax=ax1)
            ax1.set_title("Top Hashtags by Similarity Score")
            st.pyplot(fig1)

            fig2, ax2 = plt.subplots()
            sns.histplot(df["Similarity Score"], bins=10, kde=True, ax=ax2, color="skyblue")
            ax2.set_title("Distribution of Similarity Scores")
            st.pyplot(fig2)

            if tweet_texts:
                st.subheader("📥 Sample Tweets Fetched from Twitter")
                for tweet in tweet_texts[:5]:
                    st.write(tweet)

            try:
                reg, X_test, y_test, y_pred = train_regression_model(df)

                st.subheader("Regression Performance")
                st.markdown(f"**R² Score:** `{r2_score(y_test, y_pred):.4f}`")
                st.markdown(f"**MSE:** `{mean_squared_error(y_test, y_pred):.4f}`")

                fig3, ax3 = plt.subplots()
                sns.scatterplot(x=y_test, y=y_pred, ax=ax3)
                ax3.set_xlabel("Actual Similarity Score")
                ax3.set_ylabel("Predicted Similarity Score")
                ax3.set_title("Regression Prediction: Similarity Score")
                st.pyplot(fig3)
            except ValueError as ve:
                st.warning(f"Regression error: {ve}")
