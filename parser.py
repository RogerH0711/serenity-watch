import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 初始化新版 Gemini 客戶端
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def parse_tweets():
    try:
        with open("raw_tweets.json", "r", encoding="utf-8") as f:
            tweets = json.load(f)
    except FileNotFoundError:
        print("錯誤：找不到 raw_tweets.json")
        return

    parsed_results = []
    print(f"開始解析共 {len(tweets)} 則推文...")

    system_instruction = (
        "你是一個專業的半導體與供應鏈分析助手。請將分析結果嚴格依據以下 JSON 格式輸出：\n"
        "{\n"
        "  \"has_stock_mention\": true/false,\n"
        "  \"mentions\": [\n"
        "    {\n"
        "      \"ticker\": \"股票代碼 (例如 NVDA, AXTI)\",\n"
        "      \"sentiment\": \"Bullish / Bearish / Neutral\",\n"
        "      \"thesis\": \"核心論點摘要 (50字內)\",\n"
        "      \"risks\": \"提及的風險 (若無則寫 null)\"\n"
        "    }\n"
        "  ]\n"
        "}"
    )

    for idx, tweet in enumerate(tweets):
        text = tweet.get("text", "")
        timestamp = tweet.get("timestamp", "")
        url = tweet.get("url", "")

        if not text:
            continue

        prompt = f"請分析以下推文，提取其中提及的半導體或AI相關股票代碼（Ticker）。針對每支提及的股票，評估作者的情緒態度，並摘要核心論點與風險。\n\n推文內容：\n{text}"

        try:
            # 呼叫新版 API 與 gemini-2.5-flash 模型
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    temperature=0.1
                )
            )
            
            analysis = json.loads(response.text)

            if analysis.get("has_stock_mention") and analysis.get("mentions"):
                for mention in analysis["mentions"]:
                    parsed_results.append({
                        "timestamp": timestamp,
                        "url": url,
                        "ticker": str(mention.get("ticker")).upper(),
                        "sentiment": mention.get("sentiment"),
                        "thesis": mention.get("thesis"),
                        "risks": mention.get("risks")
                    })
            print(f"[{idx+1}/{len(tweets)}] 解析完成")

        except Exception as e:
            print(f"[{idx+1}/{len(tweets)}] 解析失敗: {e}")
            continue

    with open("parsed_tweets.json", "w", encoding="utf-8") as f:
        json.dump(parsed_results, f, ensure_ascii=False, indent=4)

    print(f"數據結構化完成！已儲存 {len(parsed_results)} 筆紀錄至 parsed_tweets.json")

if __name__ == "__main__":
    parse_tweets()