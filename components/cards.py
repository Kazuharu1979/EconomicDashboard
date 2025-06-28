import streamlit as st
from urllib.parse import quote

def get_color_by_change(change):
    try:
        c = float(change)
    except:
        c = 0.0
    strength = min(abs(c) / 10, 1.0)
    if c > 0:
        return f"rgba(0, 200, 0, {0.1 + 0.4 * strength})"
    elif c < 0:
        return f"rgba(255, 0, 0, {0.1 + 0.4 * strength})"
    else:
        return "rgba(200, 200, 200, 0.2)"

def render_metric_card(label, value, change, change_text, last_date):
    color = get_color_by_change(change)
    try:
        c = float(change)
    except:
        c = 0.0
    value_color = "#006400" if c > 0 else "#8B0000" if c < 0 else "#1c1c1c"
    label_encoded = quote(label)

    html = f"""
    <div style='
        background-color: {color};
        padding: 1rem 1.2rem;
        border-radius: 0.5rem;
        text-align: left;
        margin: 0.5rem;
        border: 1px solid #e6e6e6;
    '>
        <div style='font-weight: 600; font-size: 1rem;'>{label}</div>
        <div style='font-size: 1.4rem; font-weight: 700; color: {value_color};'>{value}</div>
        <div style='font-size: 0.9rem; color: #5c5c5c; margin-top: 0.3rem;'>{change_text}</div>
        <div style='font-size: 0.8rem; color: #999; margin-top: 0.3rem;'>更新日: {last_date}</div>
        <div style='margin-top: 0.4rem;'>
            <a href="/detail_chart?symbol={label_encoded}" style='text-decoration: none;'>📈 詳細グラフへ</a>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)