import streamlit as st
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def select_date_range(today=None):
    if today is None:
        today = datetime.today().date()

    preset_options = {
        "前日比": 1,
        "1週間": timedelta(weeks=1),
        "1か月": relativedelta(months=1),
        "3か月": relativedelta(months=3),
        "1年": relativedelta(years=1),
        "5年": relativedelta(years=5),
        "10年": relativedelta(years=10),
        "カスタム": None
    }

    range_option = st.sidebar.selectbox("表示期間（プリセット）", list(preset_options.keys()), index=0)

    if range_option == "カスタム":
        default_start = today - timedelta(days=30)
        start_date = st.sidebar.date_input("開始日", value=default_start, max_value=today)
        end_date = st.sidebar.date_input("終了日", value=today, min_value=start_date, max_value=today)
    else:
        delta = preset_options.get(range_option)
        end_date = today
        start_date = end_date - (timedelta(days=2) if range_option == "前日比" else delta)
        st.sidebar.date_input("開始日", value=start_date, disabled=True)
        st.sidebar.date_input("終了日", value=end_date, disabled=True)

    return range_option, datetime.combine(start_date, datetime.min.time()), datetime.combine(end_date, datetime.min.time())
