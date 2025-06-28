import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from config.indicators import indicators_by_category
from data.fetcher import fetch_data, fetch_japan_bond_yield_mof
import plotly.graph_objects as go

# クエリパラメータから対象ラベルを取得
query_params = st.query_params
symbol = query_params.get("symbol", "")

if not symbol:
    st.warning("表示する指標が指定されていません。")
    st.stop()

label = symbol

# ページ設定
st.set_page_config(page_title="詳細グラフ", layout="wide")
st.title(f"📈 {label} 詳細")

# ラベルからカテゴリ付きの情報を逆引き
label_to_info = {}
for cat, group in indicators_by_category.items():
    for lbl, inf in group.items():
        label_to_info[lbl] = {**inf, "category": cat}

info = label_to_info.get(label)

if not info:
    st.error(f"{label} の情報が見つかりません。")
    st.stop()

category = info.get("category", "")
today = datetime.today().date()

# ✅ 表示期間プリセットとカスタム日付の切り替え
preset_options = {
    "1週間": timedelta(weeks=1),
    "1か月": relativedelta(months=1),
    "3か月": relativedelta(months=3),
    "1年": relativedelta(years=1),
    "5年": relativedelta(years=5),
    "10年": relativedelta(years=10),
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

start_date_display = datetime.combine(start_date, datetime.min.time())
end_date_display = datetime.combine(end_date, datetime.min.time())

# ✅ 移動平均の設定（サイドバー）
show_ma = st.sidebar.checkbox("移動平均線を表示", value=True)
ma_periods = st.sidebar.multiselect("移動平均期間（日）", [5, 10, 20, 25, 50, 75, 100, 200, 360], default=[5, 20])

# 移動平均用にデータ取得期間を延長
fetch_start_date = start_date_display - timedelta(days=360 + max(ma_periods, default=0))

# データ取得
if info.get("is_mof"):
    df = fetch_japan_bond_yield_mof(fetch_start_date, end_date_display, term=info.get("term", "10年"))
else:
    df = fetch_data(info["ticker"], fetch_start_date, end_date_display)

if df.empty:
    st.warning(f"{label} のデータが取得できませんでした。")
    st.stop()

# 'Close' 列に揃える
if "Close" not in df.columns:
    if df.shape[1] == 1:
        df.columns = ["Close"]
    else:
        st.error("このデータには 'Close' 相当の列が見つかりません。")
        st.write("データ列名一覧:", df.columns.tolist())
        st.stop()

# 移動平均を計算
if show_ma:
    for period in ma_periods:
        df[f"MA{period}"] = df["Close"].rolling(window=period).mean()

# 表示範囲でフィルタリング
df_display = df[df.index >= start_date_display]

# ✅ グラフ描画
try:
    fig = go.Figure()

    # 終値（実線）
    fig.add_trace(go.Scatter(
        x=df_display.index,
        y=df_display["Close"],
        mode="lines",
        name="終値",
        line=dict(dash="solid")
    ))

    # 移動平均（点線）
    if show_ma:
        for period in ma_periods:
            ma_col = f"MA{period}"
            fig.add_trace(go.Scatter(
                x=df_display.index,
                y=df_display[ma_col],
                mode="lines",
                name=f"{period}日移動平均",
                line=dict(dash="dot")
            ))

    # 縦軸タイトルの設定
    yaxis_label = "利回り（％）" if category == "国債" else "価格"

    fig.update_layout(
        title=label,
        xaxis_title="日付",
        yaxis_title=yaxis_label,
        xaxis=dict(tickformat="%Y/%m/%d"),
        legend=dict(x=0, y=1)
    )

    st.plotly_chart(fig, use_container_width=True)

    # ✅ 解説文の表示（展開状態）
    description = info.get("description")
    if description:
        with st.expander("ℹ️ 指標の解説", expanded=True):
            st.markdown(description)

except Exception as e:
    st.error(f"{label} のグラフ描画中にエラーが発生しました: {e}")
