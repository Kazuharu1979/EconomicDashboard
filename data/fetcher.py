import yfinance as yf
import pandas as pd
import streamlit as st
from datetime import datetime
import re
import time

@st.cache_data(ttl=3600)  # 1時間キャッシュ
def fetch_data(ticker, start_date, end_date, retries=3, delay=2):
    for attempt in range(retries):
        try:
            df = yf.download(ticker, start=start_date, end=end_date, progress=False)

            # MultiIndex の場合はフラット化
            if isinstance(df.columns, pd.MultiIndex):
                try:
                    df = df.xs(ticker, level=1, axis=1)
                except KeyError:
                    raise ValueError(f"{ticker} のデータが見つかりません。")

            if 'Close' not in df.columns:
                raise ValueError(f"{ticker} の終値データが存在しません。")

            df = df[['Close']].dropna()
            df.index = pd.to_datetime(df.index)
            df.index.name = "date"
            return df

        except Exception as e:
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                st.warning(f"{ticker} のデータ取得に繰り返し失敗しました。エラー内容: {e}")
                return pd.DataFrame()

def convert_wareki_to_datetime(wareki_str):
    if not isinstance(wareki_str, str):
        return None
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
        "E": 2018,  # Excel変換用
    }
    base = era_offset.get(era)
    if base is None:
        return None
    return datetime(base + year, month, day)

@st.cache_data(ttl=86400)  # 1日キャッシュ
def load_mof_raw_data():
    url_all = "https://www.mof.go.jp/jgbs/reference/interest_rate/data/jgbcm_all.csv"
    url_current = "https://www.mof.go.jp/jgbs/reference/interest_rate/jgbcm.csv"

    df_all = pd.read_csv(url_all, encoding="shift_jis", header=1)
    df_current = pd.read_csv(url_current, encoding="shift_jis", header=1)

    df_all["date"] = df_all["基準日"].apply(convert_wareki_to_datetime)
    df_current["date"] = df_current["基準日"].apply(convert_wareki_to_datetime)

    return df_all, df_current

@st.cache_data(ttl=86400)  # 1日キャッシュ
def fetch_japan_bond_yield_mof(start_date, end_date, term="10年"):
    try:
        df_all, df_current = load_mof_raw_data()

        common_cols = [col for col in df_all.columns if col in df_current.columns]
        df_all = df_all[common_cols]
        df_current = df_current[common_cols]

        df = pd.concat([df_all, df_current], ignore_index=True)
        df = df.dropna(subset=["date"])
        df = df.sort_values("date").drop_duplicates("date")

        if term not in df.columns:
            return pd.DataFrame()

        df = df[["date", term]].dropna()
        df[term] = pd.to_numeric(df[term].replace("-", pd.NA), errors="coerce")
        df = df.dropna()
        df = df.set_index("date").astype(float)
        df.columns = [f"JPY{term}"]

        return df.loc[start_date:end_date].sort_index()

    except Exception as e:
        st.error(f"MOFデータ取得エラー: {e}")
        return pd.DataFrame()