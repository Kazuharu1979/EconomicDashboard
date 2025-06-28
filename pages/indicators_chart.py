import streamlit as st
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pandas as pd
import plotly.express as px
from config.indicators import indicators_by_category
from data.fetcher import fetch_data, fetch_japan_bond_yield_mof
from utils.chart import plot_comparison_chart

# ページ設定
st.set_page_config(page_title="指標グラフ", layout="wide")
st.title("\U0001F4C8 指標グラフ")

# 表示期間プリセット（relativedelta 対応）
st.sidebar.markdown("### 表示期間の指定")
today = datetime.today().date()
preset_options = {
    "1週間": timedelta(weeks=1),
    "1か月": relativedelta(months=1),
    "3か月": relativedelta(months=3),
    "1年": relativedelta(years=1),
    "5年": relativedelta(years=5),
    "カスタム": None
}
preset = st.sidebar.selectbox("表示期間（プリセット）", options=list(preset_options.keys()), index=2)

if preset != "カスタム":
    delta = preset_options[preset]
    start_date = today - delta
    end_date = today
    st.sidebar.date_input("開始日", value=start_date, disabled=True)
    st.sidebar.date_input("終了日", value=end_date, disabled=True)
else:
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
        initial_index = df[label].first_valid_index()
        if initial_index is None:
            st.warning(f"{label} のデータが有効ではないため、表示できません。")
            continue
        initial_value = df.loc[initial_index, label]
        df[label] = df[label] / initial_value * 100
        combined_df = df if combined_df.empty else combined_df.join(df, how="outer")

    for ticker in custom_tickers:
        df = fetch_data(ticker, start_date, end_date)
        if df.empty:
            st.warning(f"カスタム: {ticker} のデータが取得できませんでした。")
            continue
        label = f"カスタム: {ticker}"
        df = df.rename(columns={df.columns[0]: label})
        df[label] = pd.to_numeric(df[label], errors="coerce")
        initial_index = df[label].first_valid_index()
        if initial_index is None:
            st.warning(f"カスタム: {ticker} のデータが有効ではないため、表示できません。")
            continue
        initial_value = df.loc[initial_index, label]
        df[label] = df[label] / initial_value * 100
        combined_df = combined_df.join(df, how="outer")

    if not combined_df.empty:
        combined_df = combined_df.sort_index().interpolate(method="linear")
        fig = plot_comparison_chart(combined_df)
        st.plotly_chart(fig, use_container_width=True, config={"renderer": "svg"})
    else:
        st.info("表示できるデータがありません。")

# 個別グラフ
else:
    all_labels = st.session_state.selected_labels + [f"カスタム: {t}" for t in custom_tickers]
    for i, label in enumerate(all_labels):
        with st.container():
            if label.startswith("カスタム: "):
                ticker = label.replace("カスタム: ", "")
                df = fetch_data(ticker, start_date, end_date)
            else:
                info = label_to_info[label]
                if info.get("is_mof"):
                    df = fetch_japan_bond_yield_mof(start_date, end_date, term=info.get("term", "10年"))
                else:
                    df = fetch_data(info["ticker"], start_date, end_date)

            st.subheader(label)
            if df.empty:
                st.warning(f"{label} のデータが取得できませんでした。")
            else:
                try:
                    df_plot = df.copy()
                    df_plot["date"] = df_plot.index
                    df_plot = df_plot.dropna(subset=[df.columns[0]])
                    if df_plot.empty:
                        st.warning(f"{label} の有効なデータが存在しないため、グラフが表示できません。")
                        continue
                    # 5年表示のときは週単位に間引く
                    if preset == "5年":
                        df_plot = df_plot.set_index("date").resample("W").mean().reset_index()
                    fig = px.line(df_plot, x="date", y=df.columns[0])
                    st.plotly_chart(fig, use_container_width=True, config={"renderer": "svg"})
                except Exception as e:
                    st.error(f"{label} のグラフ描画中にエラーが発生しました: {e}")
