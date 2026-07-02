import sqlite3
import json
from datetime import datetime

def build_static_site():
    # 1. 從資料庫讀取所有紀錄
    conn = sqlite3.connect("serenity.db")
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, ticker, sentiment, thesis, risks, url FROM mentions ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("資料庫內無資料。")
        return

    # 2. 按 Ticker 進行分組聚合 (確保首頁每檔股票只有一張卡片)
    aggregated_data = {}
    for row in rows:
        timestamp, ticker, sentiment, thesis, risks, url = row
        if ticker not in aggregated_data:
            aggregated_data[ticker] = {
                "latest_timestamp": timestamp[:10],
                "latest_sentiment": sentiment,
                "posts": []
            }
        
        # 將該股票所有的發言紀錄存起來
        aggregated_data[ticker]["posts"].append({
            "d": timestamp[:10],
            "tag": sentiment,
            "text": f"【論點】\n{thesis}\n\n【風險】\n{risks if risks else '未提及'}",
            "url": url
        })

    # 3. 生成首頁的 HTML 卡片與彈出視窗用的 JSON
    cards_html = ""
    dd_data = {}

    for ticker, info in aggregated_data.items():
        # 設定 CSS 顏色
        stance_class = "neutral"
        if info["latest_sentiment"] == "Bullish":
            stance_class = "bull"
        elif info["latest_sentiment"] == "Bearish":
            stance_class = "bear"

        # 取最新的一條論點顯示在首頁卡片上
        latest_thesis = info["posts"][0]["text"].split("【風險】")[0].replace("【論點】\n", "")

        # 組合 HTML 卡片
        cards_html += f"""
        <div class="card {stance_class}" onclick="dd('{ticker}')">
            <div>
                <span class="tk">{ticker}</span>
                <span class="badge {stance_class}">{info["latest_sentiment"]}</span>
            </div>
            <div class="csumm">{latest_thesis[:80]}...</div>
            <div style="font-size:11px; color:gray; margin-top:15px;">Latest: {info["latest_timestamp"]}</div>
        </div>
        """

        # 將該股票的所有歷史紀錄放進 JSON
        dd_data[ticker] = {
            "posts": info["posts"]
        }

    # 4. 讀取模板並替換
    try:
        with open("template.html", "r", encoding="utf-8") as f:
            template = f.read()
    except FileNotFoundError:
        print("錯誤：找不到 template.html")
        return

    html_output = template.replace("{{ DAILY_CARDS }}", cards_html)
    json_str = json.dumps(dd_data, ensure_ascii=False)
    html_output = html_output.replace("{{ DYNAMIC_JSON_DATA }}", json_str)

    # 5. 輸出靜態網頁
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_output)
    
    print(f"網頁生成成功！共有 {len(aggregated_data)} 檔股票。")

if __name__ == "__main__":
    build_static_site()