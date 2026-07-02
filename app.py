import streamlit as st
import sqlite3
import pandas as pd
import os
from google import genai
from dotenv import load_dotenv

# 載入環境變數與初始化 Gemini 客戶端
load_dotenv()
try:
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
except Exception as e:
    st.error("請確認 .env 檔案中已正確設定 GEMINI_API_KEY")

# 頁面基本設定
st.set_page_config(page_title="Serenity Watch", layout="wide")
st.title("🔭 Serenity Watch Dashboard")
st.markdown("追蹤 @aleabitoreddit 的公開半導體與 AI 股票分析紀錄。")

# 讀取資料庫
@st.cache_data
def load_data():
    conn = sqlite3.connect("serenity.db")
    query = "SELECT timestamp, ticker, sentiment, thesis, risks, url FROM mentions ORDER BY timestamp DESC"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

df = load_data()

if df.empty:
    st.warning("目前資料庫中沒有紀錄，請確認爬蟲與解析腳本已正確執行。")
else:
    # 建立側邊欄過濾器
    st.sidebar.header("條件篩選")
    tickers = sorted(df['ticker'].unique().tolist())
    selected_ticker = st.sidebar.selectbox("選擇股票代碼 (Ticker)", ["All"] + tickers)

    # 依照選擇過濾資料
    if selected_ticker != "All":
        filtered_df = df[df['ticker'] == selected_ticker]
    else:
        filtered_df = df

    # 使用 Tabs 將「儀表板」與「AI 問答」分開
    tab1, tab2 = st.tabs(["📊 數據儀表板", "🤖 AI 標的分析 (RAG)"])

    with tab1:
        st.subheader(f"分析紀錄 ({selected_ticker})")
        display_df = filtered_df.copy()
        display_df.columns = ["時間", "股票代碼", "市場情緒", "核心論點", "風險因素", "原文連結"]
        st.dataframe(display_df, use_container_width=True, hide_index=True)

        st.subheader("市場情緒分佈")
        sentiment_counts = filtered_df['sentiment'].value_counts()
        st.bar_chart(sentiment_counts)

    with tab2:
        st.subheader("向 AI 詢問標的細節")
        st.markdown("基於歷史推文資料庫，AI 將為您總結該標的之投資論點、情緒變化與潛在風險。")
        
        # RAG 查詢介面
        if selected_ticker == "All":
            st.info("💡 請先在左側邊欄選擇一個特定的股票代碼（例如：META），才能進行針對性問答。")
        else:
            user_question = st.text_input(f"關於 {selected_ticker}，你想了解什麼？", placeholder=f"例如：{selected_ticker} 最大的風險是什麼？")
            
            if st.button("生成分析報告") and user_question:
                with st.spinner("AI 正在檢索資料庫並生成回覆..."):
                    # 1. 檢索 (Retrieval): 將過濾後的 DataFrame 轉為文字 Context
                    context_lines = []
                    for index, row in filtered_df.iterrows():
                        context_lines.append(
                            f"- 時間: {row['timestamp']}\n  情緒: {row['sentiment']}\n  論點: {row['thesis']}\n  風險: {row['risks']}\n  來源: {row['url']}"
                        )
                    context_text = "\n\n".join(context_lines)
                    
                    # 2. 增強與生成 (Augmented Generation)
                    prompt = f"""
                    你是一個專業的 AI 半導體與供應鏈投資助手。
                    請「僅根據以下提供的歷史紀錄資料庫」，回答使用者的問題。
                    如果在提供的資料中找不到答案，請誠實回答「歷史紀錄中未提及此資訊」，不要自行捏造數據。
                    在回覆時，請盡量附上觀點對應的「時間」以增加可信度。

                    【歷史紀錄資料庫】
                    {context_text}

                    【使用者問題】
                    {user_question}
                    """

                    try:
                        response = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=prompt
                        )
                        st.markdown("### 📝 分析結果")
                        st.write(response.text)
                        
                        with st.expander("🔍 查看 AI 參考的原始數據 (Context)"):
                            st.text(context_text)
                            
                    except Exception as e:
                        st.error(f"生成回覆時發生錯誤：{e}")