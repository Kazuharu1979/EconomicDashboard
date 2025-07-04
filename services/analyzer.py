import openai
import os
import streamlit as st
import hashlib
import json

openai.api_key = os.environ["OPENAI_API_KEY"]

def _make_cache_key(changes_by_label, news_summaries, start_date, end_date):
    """キャッシュキーを安定化させるためのハッシュ関数"""
    key_data = {
        "changes": changes_by_label,
        "news": news_summaries,
        "start": str(start_date.date()),
        "end": str(end_date.date())
    }
    key_str = json.dumps(key_data, sort_keys=True, ensure_ascii=False)
    return hashlib.md5(key_str.encode("utf-8")).hexdigest()

@st.cache_data(ttl=1800, show_spinner="ChatGPTで分析中...")
def generate_analysis(changes_by_label, news_summaries, start_date, end_date):
    try:
        cache_key = _make_cache_key(changes_by_label, news_summaries, start_date, end_date)

        summary_prompt = f"""
以下は世界経済に関する指標の変化率データです。
分析対象期間は {start_date.date()} から {end_date.date()} です。
この情報に加えて、期間中に報道された重要ニュースやWebの情報も参考にして、現在の世界経済の動向と注目ポイントを日本語で簡潔に分析してください。
特に、指標の動きと関連しそうなニュースを取り上げてください。
出力には「分析対象期間」という表現は使わず、「前日比」「1カ月」「約3カ月」など、一般的な表現を用いてください。
語尾は、ですます調に統一してください。

【指標の変化率】
"""
        for label, changes in changes_by_label.items():
            summary_prompt += f"- {label}:"
            summary_prompt += f"  - 直近5日: {changes.get('5d', 0):+.2f}%\n"
            summary_prompt += f"  - 過去1か月: {changes.get('1mo', 0):+.2f}%\n"
            summary_prompt += f"  - 過去3か月: {changes.get('3mo', 0):+.2f}%\n"
            summary_prompt += f"  - 分析対象期間: {changes.get('range', 0):+.2f}%\n"

        if news_summaries:
            summary_prompt += "\n【期間中の主な経済ニュース】\n"
            summary_prompt += "\n".join([f"- {news}" for news in news_summaries[:50]])

        summary_prompt += "\n\n注目すべきポイントを3つ程度、箇条書きで示してください。"

        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "あなたは世界経済を分析する有能なアナリストです。"},
                {"role": "user", "content": summary_prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"コメント生成中にエラーが発生しました: {e}"
