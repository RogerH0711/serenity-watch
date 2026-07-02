以下為專案的 README.md 內容。請直接複製下方 Markdown 區塊貼上至你的 README.md 檔案中。

```markdown
# Serenity Watch 🔭

Serenity Watch 是一個自動化 X (原 Twitter) 貼文追蹤與分析系統。本專案透過自動化腳本擷取特定分析師的公開推文，利用大語言模型 (LLM) 進行結構化數據解析，並提供一個基於 RAG (檢索增強生成) 架構的互動式儀表板，以利快速掌握特定標的之歷史觀點與潛在風險。

## 系統架構

* **資料擷取 (Data Ingestion)**: Python `Playwright` (繞過前端登入限制，無頭瀏覽器抓取)
* **資料解析 (Data Structuring)**: Google `Gemini-2.5-flash` API (將純文本轉換為包含情緒、論點與風險的 JSON 格式)
* **資料儲存 (Database)**: `SQLite` (輕量級關聯式資料庫)
* **前端展示與問答 (Frontend & RAG)**: `Streamlit` (互動式數據儀表板與 AI 問答介面)

## 快速開始指南

以下步驟將引導你在本機端環境從零開始建置並運行此專案。

### 1. 系統需求
* Python 3.8 或以上版本
* Google 帳號 (用於申請 Gemini API Key)
* 電腦中已安裝 Google Chrome 或 Microsoft Edge 瀏覽器 (用於取得 X 平台的驗證 Cookie)

### 2. 環境安裝

首先，將專案複製到本機並進入目錄：
```bash
git clone [https://github.com/你的帳號/serenity-watch.git](https://github.com/你的帳號/serenity-watch.git)
cd serenity-watch

```

建立並啟動虛擬環境 (Virtual Environment)：

```bash
# macOS / Linux
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate

```

安裝所需的 Python 套件與 Playwright 瀏覽器核心：

```bash
pip install -r requirements.txt
playwright install

```

### 3. 環境變數設定 (.env)

本專案需要兩組金鑰才能運行。請在專案根目錄下建立一個名為 `.env` 的檔案，並填入以下內容：

```env
# Google Gemini API 金鑰
GEMINI_API_KEY=your_gemini_api_key_here

# X (Twitter) 登入憑證
X_AUTH_TOKEN=your_x_auth_token_here

```

**如何取得金鑰？**

* **GEMINI_API_KEY**: 前往 [Google AI Studio](https://aistudio.google.com/) 免費申請。
* **X_AUTH_TOKEN**:
1. 在瀏覽器中登入你的 X (Twitter) 帳號。
2. 按下 `F12` 或右鍵點擊「檢查」開啟開發者工具。
3. 切換至 `Application` (應用程式) 標籤。
4. 在左側欄展開 `Cookies` 並點擊 `https://x.com`。
5. 在右側列表中找到名稱為 `auth_token` 的項目，複製其 Value 並貼入 `.env` 檔案中。



### 4. 執行資料管線 (Data Pipeline)

在啟動網頁介面之前，需先抓取並建立資料庫。你可以執行自動化腳本，或依序執行 Python 檔案：

**方法 A：使用 Shell 腳本 (推薦 macOS/Linux)**

```bash
chmod +x run_pipeline.sh
./run_pipeline.sh

```

**方法 B：手動依序執行**

```bash
python scraper.py   # 1. 抓取最新推文
python parser.py    # 2. 透過 LLM 解析數據
python db_setup.py  # 3. 寫入 SQLite 資料庫

```

### 5. 啟動互動式儀表板

資料建立完成後，啟動 Streamlit 伺服器：

```bash
streamlit run app.py

```

終端機將會顯示一組 Local URL (通常為 `http://localhost:8501`)，點擊網址即可在瀏覽器中操作系統。

## 專案目錄結構

```text
serenity-watch/
├── .env                  # 環境變數與機密金鑰 (請勿上傳)
├── .gitignore            # Git 忽略清單
├── README.md             # 專案說明文件
├── requirements.txt      # Python 相依套件清單
├── run_pipeline.sh       # 管線自動化執行腳本
├── scraper.py            # Playwright 爬蟲腳本
├── parser.py             # Gemini API 結構化解析腳本
├── db_setup.py           # SQLite 資料庫初始化與寫入腳本
└── app.py                # Streamlit 前端與 RAG 應用程式

```

## 免責聲明

本專案僅作為技術研究與公開資訊整理介面。系統產出之情緒標籤與總結內容皆由 AI 自動生成，可能存在誤差，**不構成任何財務或投資建議**。進行任何決策前，請務必點擊原文連結確認原始資訊。

```

```