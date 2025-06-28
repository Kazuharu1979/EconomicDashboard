import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta
import streamlit as st  # 追加：キャッシュ用

load_dotenv()

API_KEY = os.getenv("MARKETAUX_API_KEY")
BASE_URL = "https://api.marketaux.com/v1/news/all"

# 世界経済に影響を与える英語キーワード一覧
KEYWORDS_EN = [
    "Federal Reserve", "interest rate", "inflation", "GDP", "employment", "unemployment",
    "consumer spending", "manufacturing", "recession", "stimulus", "ECB", "BOJ", "IMF",
    "oil prices", "commodity prices", "supply chain", "China economy", "US economy",
    "geopolitical risk", "trade war", "bond yields", "stock market"
]

@st.cache_data(ttl=1800)  # 30分キャッシュ
def fetch_market_news(start_date=None, end_date=None):
    # デフォルト期間：過去1日
    if start_date is None:
        start_date = datetime.utcnow() - timedelta(days=1)
    if end_date is None:
        end_date = datetime.utcnow()

    start_iso = start_date.replace(hour=0, minute=0, second=0, microsecond=0).strftime("%Y-%m-%dT%H:%M:%S")
    end_iso = end_date.replace(hour=0, minute=0, second=0, microsecond=0).strftime("%Y-%m-%dT%H:%M:%S")

    keyword_query = "|".join(KEYWORDS_EN)
    params = {
        "api_token": API_KEY,
        "search": keyword_query,
        "countries": "us,cn,jp,eu,de,gb",
        "language": "en",
        "limit": 50,
        "published_after": start_iso,
        "published_before": end_iso,
        "sort_by": "relevance_score",
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if "data" not in data:
            return []

        articles = data["data"]
        summaries = [
            f"{a['title']} ({a['published_at'][:10]})\n{a['description']}"
            for a in articles if a.get("title") and a.get("description")
        ]
        return summaries
    except Exception as e:
        return [f"[ニュース取得エラー]: {e}"]
