import plotly.express as px

def plot_comparison_chart(df, title="\U0001F4C8 指標の相対変化比較グラフ"):
    fig = px.line(
        df,
        x=df.index,
        y=df.columns,
        labels={"value": "変化率（初期値=100）", "variable": "指標"},
        title=title
    )
    return fig