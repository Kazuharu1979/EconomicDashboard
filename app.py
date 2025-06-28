import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from config.indicators import indicators_by_category, category_order
from data.fetcher import fetch_data, fetch_japan_bond_yield_mof
from data.news_fetcher import fetch_market_news
from components.selector import select_date_range
from components.cards import render_metric_card
from services.analyzer import generate_analysis
import pytz

st.set_page_config(page_title="世界経済ダッシュボード", layout="wide")
st.title("🌐 世界経済ダッシュボード")

# 日付選択
range_option, start_date, end_date = select_date_range()

# 各指標の変化率格納用
label_changes = {}

# 各カテゴリごとに指標を描画
for category in category_order:
    items = indicators_by_category.get(category, {})
    if not items:
        continue

    st.markdown(f"### {category}")
    cols = st.columns(4)
    i = 0

    for label, info in items.items():
        try:
            if info.get("is_mof"):
                df = fetch_japan_bond_yield_mof(start_date - timedelta(days=7), end_date, term=info.get("term", "10年"))
            else:
                df = fetch_data(info["ticker"], start_date - timedelta(days=7), end_date)

            if df.empty:
                st.warning(f"{label} のデータが空です。")
                continue

            df_in_range = df[df.index <= end_date]

            if range_option == "前日比":
                if len(df_in_range) < 2:
                    st.warning(f"{label} の期間内データが不十分です。")
                    continue
                prev_value = df_in_range.iloc[-2, 0]
                end_value = df_in_range.iloc[-1, 0]
            else:
                df_period = df[(df.index >= start_date) & (df.index <= end_date)]
                if len(df_period) < 2:
                    st.warning(f"{label} の指定期間データが不十分です。")
                    continue
                prev_value = df_period.iloc[0, 0]
                end_value = df_period.iloc[-1, 0]

            if info.get("is_mof"):
                change = end_value - prev_value
                change_text = f"{change:+.2f}%"
            else:
                change = ((end_value - prev_value) / prev_value) * 100
                change_text = f"{change:+.2f}%（変化率）"

            label_changes[label] = change

            last_date = df_in_range.index[-1].tz_localize("UTC").tz_convert("Asia/Tokyo").strftime("%Y-%m-%d")

            with cols[i % 4]:
                render_metric_card(label, f"{end_value:.2f}", change, change_text, last_date)
            i += 1

        except Exception as e:
            st.warning(f"{label} の取得中にエラーが発生しました: {e}")

# ニュース取得（期間調整）
if range_option == "前日比":
    news_start = datetime.combine(end_date.date() - timedelta(days=1), datetime.min.time())
    news_end = datetime.combine(end_date.date() + timedelta(days=1), datetime.min.time())
else:
    news_start = start_date
    news_end = end_date + timedelta(days=1)

news_summaries = fetch_market_news(news_start, news_end)

# ChatGPTによる要約分析
st.markdown("---")
st.markdown("### 🤖 ChatGPTによる市場分析コメント")
st.info("個別指標の変化率と最近のニュースをもとに、世界経済の動向を自動で分析します。")

comment = generate_analysis(label_changes, news_summaries, start_date, end_date)
st.markdown(comment)

# ニューステーブル表示
def parse_summary(summary):
    try:
        title_line, description = summary.split("\n", 1)
        title, date = title_line.rsplit("(", 1)
        return {
            "タイトル": title.strip(),
            "日付": date.replace(")", "").strip(),
            "要約": description.strip()
        }
    except:
        return {
            "タイトル": summary,
            "日付": "",
            "要約": ""
        }

parsed_news = [parse_summary(n) for n in news_summaries]
df_news = pd.DataFrame(parsed_news)
df_news.index = df_news.index + 1
df_news.index.name = "No"

if not df_news.empty:
    st.markdown("### 📰 参考ニュース一覧")
    st.markdown(
        """
        <style>
        table th:nth-child(1), table td:nth-child(3) {
            white-space: nowrap;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.table(df_news)