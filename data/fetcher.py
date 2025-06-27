import yfinance as yf
import pandas as pd
import streamlit as st
from datetime import datetime
import re

def fetch_data(ticker, start_date, end_date):
    df = yf.download(ticker, start=start_date, end=end_date)

    # MultiIndex の場合はフラット化
    if isinstance(df.columns, pd.MultiIndex):
        try:
            df = df.xs(ticker, level=1, axis=1)
        except KeyError:
            st.warning(f"{ticker} のデータが取得できませんでした。")
            return pd.DataFrame()

    # 必要なカラムがあるか確認
    if 'Close' not in df.columns:
        st.warning(f"{ticker} の終値データが存在しません。")
        return pd.DataFrame()

    # 終値のみ抽出し、インデックス名を設定
    df = df[['Close']].dropna()
    df.index = pd.to_datetime(df.index)
    df.index.name = "date"
    return df
    
# ✅ 修正：datetime.datetime → datetime
def convert_wareki_to_datetime(wareki_str):
    match = re.match(r"([MTSHRE])(\d+)\.(\d+)\.(\d+)", wareki_str)
    if not match:
        return None
    era, year, month, day = match.groups()
    year, month, day = int(year), int(month), int(day)

    era_offset = {
        "M": 1867,  # 明治
        "T": 1911,  # 大正
        "S": 1925,  # 昭和
        "H": 1988,  # 平成
        "R": 2018,  # 令和
        "E": 2018,  # Excel誤変換対策
    }
    base = era_offset.get(era)
    if base is None:
        return None
    return datetime(base + year, month, day)

# 財務省CSVから指定年限の利回りを取得
def fetch_japan_bond_yield_mof(start_date, end_date, term="10年"):
    try:
        url = "https://www.mof.go.jp/jgbs/reference/interest_rate/data/jgbcm_all.csv"
        df = pd.read_csv(url, encoding="shift_jis", header=1)

        df["date"] = df["基準日"].apply(convert_wareki_to_datetime)
        df = df.dropna(subset=["date"])
        df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]

        if term not in df.columns:
            return pd.DataFrame()

        df = df[["date", term]].dropna()
        df[term] = pd.to_numeric(df[term], errors="coerce")  # ← ★ ここで数値化
        df = df.dropna(subset=[term])

        df = df.set_index("date")
        df.columns = [f"JPY{term}"]
        df = df.sort_index()
        return df

    except Exception as e:
        print(f"データ取得エラー: {e}")
        return pd.DataFrame()

