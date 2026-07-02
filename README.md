# Serenity Watch 🔭 (Static Edition)

Serenity Watch 是一個自動化 X (原 Twitter) 貼文追蹤與分析系統。本專案透過自動化腳本擷取特定分析師的公開推文，利用大語言模型 (LLM) 進行結構化數據解析，並將結果編譯為極簡、高效的純靜態 HTML 網頁 (Static Site)，方便快速掌握特定標的之歷史觀點與潛在風險。

## 系統架構 (Data Pipeline)

本專案採用無伺服器 (Serverless-friendly) 的靜態生成架構：

1. **Data Ingestion**: Python `Playwright` 繞過前端限制進行無頭瀏覽器抓取。
2. **Data Structuring**: Google `Gemini-2.5-flash` API 將純文字轉換為結構化 JSON (提取標的、情緒、論點、風險)。
3. **Database**: `SQLite` 負責資料持久化與去重。
4. **Static Site Generation (SSG)**: Python 腳本將 SQLite 資料聚合，並動態注入至 `template.html`，產出純前端 `index.html`。

## 快速開始指南

### 1. 系統需求 & 環境安裝
* Python 3.8+
* Google Chrome 或 Microsoft Edge (用於取得 X 平台的驗證 Cookie)

將專案 clone 到本機並啟動虛擬環境：
```bash
git clone https://github.com/RogerH0711/serenity-watch
cd serenity-watch
python -m venv venv
source venv/bin/activate  # Windows 請用 venv\Scripts\activate
```
安裝相依套件與瀏覽器驅動：
```Bash
pip install -r requirements.txt
playwright install
```
2. 環境變數設定 (.env)
在專案根目錄下建立 .env 檔案，填入以下金鑰：

程式碼片段
# Google AI Studio API Key
GEMINI_API_KEY=your_gemini_api_key_here

# X (Twitter) auth_token (從瀏覽器開發者工具的 Cookies 中獲取)
X_AUTH_TOKEN=your_x_auth_token_here

3. 執行自動化管線
本專案提供了一鍵執行的 Shell 腳本，會依序執行爬蟲、AI 解析、資料庫寫入，並生成最終網頁：
```Bash
chmod +x run_pipeline.sh
./run_pipeline.sh
```
執行完畢後，直接在瀏覽器中打開專案目錄下的 index.html 即可檢視最新儀表板。

(進階：你也可以透過 macOS 的 cron 或是 Linux 的 crontab 設定定時執行 run_pipeline.sh，實現 24 小時全自動更新。)