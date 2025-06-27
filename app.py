import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
from config.indicators import indicators_by_category
from data.fetcher import fetch_data, fetch_japan_bond_yield_mof
from utils.chart import plot_comparison_chart

# ページ設定
st.set_page_config(page_title="世界経済ダッシュボード", layout="wide")
st.title("🌐 世界経済ダッシュボード")
st.markdown("株価、為替、コモディティ、仮想通貨、国債などの主要経済指標を視覚化します。")

# 表示期間（日付指定）
st.sidebar.markdown("### 表示期間の指定")
today = datetime.today().date()
default_start = today - timedelta(days=90)
start_date = st.sidebar.date_input("開始日", value=default_start, max_value=today)
end_date = st.sidebar.date_input("終了日", value=today, min_value=start_date, max_value=today)
start_date = datetime.combine(start_date, datetime.min.time())
end_date = datetime.combine(end_date, datetime.min.time())

# 表示モード
mode = st.sidebar.radio("表示モード", ["個別グラフ", "比較グラフ（変化率）"])

# セッションステートでチェック状態を管理
if "selected_labels" not in st.session_state:
    default_selected = []
    for category, items in indicators_by_category.items():
        for label, info in items.items():
            if info.get("default", False):
                default_selected.append(label)
    st.session_state.selected_labels = default_selected

# 指標選択（カテゴリ別）
st.sidebar.markdown("### 表示する指標を選択")

# すべてクリアボタン
if st.sidebar.button("すべての選択をクリア"):
    st.session_state.selected_labels = []

for category, items in indicators_by_category.items():
    st.sidebar.markdown(f"**{category}**")
    for label, info in items.items():
        checked = st.sidebar.checkbox(label, value=label in st.session_state.selected_labels, key=label)
        if checked and label not in st.session_state.selected_labels:
            st.session_state.selected_labels.append(label)
        elif not checked and label in st.session_state.selected_labels:
            st.session_state.selected_labels.remove(label)

# カスタムティッカー入力
st.sidebar.markdown("### 任意のティッカーを入力")
custom_ticker_input = st.sidebar.text_input("カンマ区切りで複数入力可 (例: AAPL, MSFT)")
custom_tickers = [ticker.strip().upper() for ticker in custom_ticker_input.split(",") if ticker.strip()]

# ラベル→情報辞書
label_to_info = {
    label: info for group in indicators_by_category.values() for label, info in group.items()
}

# 比較グラフ（変化率）
if mode == "比較グラフ（変化率）":
    combined_df = pd.DataFrame()
    all_labels = st.session_state.selected_labels + [f"カスタム: {t}" for t in custom_tickers]

    for label in st.session_state.selected_labels:
        info = label_to_info[label]
        if info.get("is_mof"):
            df = fetch_japan_bond_yield_mof(start_date, end_date, term=info.get("term", "10年"))
        else:
            df = fetch_data(info["ticker"], start_date, end_date)
        if df.empty:
            st.warning(f"{label} のデータが取得できませんでした。")
            continue
        df = df.rename(columns={df.columns[0]: label})
        df[label] = pd.to_numeric(df[label], errors="coerce")
        df[label] = df[label] / df[label].iloc[0] * 100
        combined_df = df if combined_df.empty else combined_df.join(df, how="outer")

    for ticker in custom_tickers:
        df = fetch_data(ticker, start_date, end_date)
        if df.empty:
            st.warning(f"カスタム: {ticker} のデータが取得できませんでした。")
            continue
        df = df.rename(columns={df.columns[0]: f"カスタム: {ticker}"})
        df[f"カスタム: {ticker}"] = pd.to_numeric(df[f"カスタム: {ticker}"], errors="coerce")
        df[f"カスタム: {ticker}"] = df[f"カスタム: {ticker}"] / df[f"カスタム: {ticker}"].iloc[0] * 100
        combined_df = combined_df.join(df, how="outer")

    if not combined_df.empty:
        combined_df = combined_df.sort_index().interpolate(method="linear")
        fig = plot_comparison_chart(combined_df)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("表示できるデータがありません。")

# 個別グラフ
else:
    cols = st.columns(2)
    all_labels = st.session_state.selected_labels + [f"カスタム: {t}" for t in custom_tickers]
    for i, label in enumerate(all_labels):
        if label.startswith("カスタム: "):
            ticker = label.replace("カスタム: ", "")
            df = fetch_data(ticker, start_date, end_date)
        else:
            info = label_to_info[label]
            if info.get("is_mof"):
                df = fetch_japan_bond_yield_mof(start_date, end_date, term=info.get("term", "10年"))
            else:
                df = fetch_data(info["ticker"], start_date, end_date)

        with cols[i % 2]:
            st.subheader(label)
            if df.empty:
                st.warning(f"{label} のデータが取得できませんでした。")
            else:
                try:
                    df_plot = df.copy()
                    df_plot["date"] = df_plot.index
                    fig = px.line(df_plot, x="date", y=df.columns[0])
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error(f"{label} のグラフ描画中にエラーが発生しました: {e}")
