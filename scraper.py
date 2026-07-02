import asyncio
import json
import os
from dotenv import load_dotenv
from playwright.async_api import async_playwright
# 載入環境變數
load_dotenv()

# 設定配置
TARGET_ACCOUNT = "aleabitoreddit"
AUTH_TOKEN = os.getenv("X_AUTH_TOKEN")

if not AUTH_TOKEN:
    raise ValueError("錯誤：找不到 X_AUTH_TOKEN，請檢查 .env 檔案設定。")

async def scrape_tweets():
    async with async_playwright() as p:
        # 啟動 Chromium 瀏覽器（headless=True 代表不開啟瀏覽器視窗，背景執行）
        browser = await p.chromium.launch(headless=True)
        
        # 建立瀏覽器上下文，並注入 auth_token Cookie
        context = await browser.new_context()
        await context.add_cookies([{
            'name': 'auth_token',
            'value': AUTH_TOKEN,
            'domain': '.x.com',
            'path': '/'
        }])
        
        page = await context.new_page()
        print(f"正在前往 https://x.com/{TARGET_ACCOUNT} ...")
        
        # 前往目標使用者的推文頁面
        await page.goto(f"https://x.com/{TARGET_ACCOUNT}", wait_until="domcontentloaded")
        
        # 等待推文元件載入
        try:
            await page.wait_for_selector('article[data-testid="tweet"]', timeout=10000)
        except Exception as e:
            print("無法載入推文，請檢查 auth_token 是否過期或正確。")
            await browser.close()
            return

        tweets_data = []
        
        # 抓取頁面上的推文元件
        tweets = await page.query_selector_all('article[data-testid="tweet"]')
        print(f"成功偵測到 {len(tweets)} 則推文，開始解析...")

        for tweet in tweets:
            try:
                # 1. 抓取推文文字
                text_element = await tweet.query_selector('div[data-testid="tweetText"]')
                text = await text_element.inner_text() if text_element else ""
                
                # 2. 抓取推文時間與連結
                time_element = await tweet.query_selector('time')
                if time_element:
                    timestamp = await time_element.get_attribute('datetime')
                    # 尋找包含時間的 <a> 標籤以獲取推文網址
                    a_element = await time_element.evaluate_handle('el => el.closest("a")')
                    tweet_url = f"https://x.com{await a_element.get_attribute('href')}" if a_element else ""
                else:
                    timestamp = ""
                    tweet_url = ""

                # 濾除沒有內容的推文（例如純轉發無引言）
                if text:
                    tweets_data.append({
                        "timestamp": timestamp,
                        "text": text,
                        "url": tweet_url
                    })
            except Exception as e:
                continue

        # 儲存為 JSON 檔案
        with open("raw_tweets.json", "w", encoding="utf-8") as f:
            json.dump(tweets_data, f, ensure_ascii=False, indent=4)
        
        print(f"抓取完成！已成功儲存 {len(tweets_data)} 則推文至 raw_tweets.json")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(scrape_tweets())