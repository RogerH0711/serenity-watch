# Serenity Watch  telescope

An automated data pipeline and RAG-ready opinion tracker for semiconductor and AI supply chain analysis on X (formerly Twitter).

---

## 🎯 專案概述

**Serenity Watch** 是一個專為追蹤高價值非結構化文本（以 X 平台知名半導體分析師 `@aleabitoreddit` 為目標）所設計的端到端（End-to-End）資料工程專案。

本系統透過自動化無頭瀏覽器擷取原始貼文，利用 **Google Gemini 2.5 Flash** 大語言模型進行命名實體識別（NER）與市場情緒結構化標籤提取，最終將資料持久化儲存於本地關聯式資料庫，並自動編譯（Compile）出一套輕量、直觀且具備個股歷史脈絡追蹤功能的純前端互動式儀表板（Static HTML Dashboard）。

---

## ⚡ 核心功能

*   **無官方 API 憑證擷取**：透過自動化工具注入即時 Session Cookie，規避高額的官方 API 成本，穩定獲取推文數據。
*   **大模型結構化標籤化**：利用 LLM Structured Outputs (JSON Mode) 技術，精準提取股票代碼 (Ticker)、投資態度、核心論點與潛在風險。
*   **個股歷史脈絡歸戶**：後端自動進行 Ticker 級別的數據聚合（Aggregation），解決單一標的重複提及造成的資料冗餘。
*   **全靜態前端渲染**：最終產出物為全靜態的 `index.html` 與內嵌 JSON 數據，無需任何後端伺服器（Serverless），具備極高的載入速度與零成本部署優勢。
*   **輕量化自動管線**：內建 Shell 腳本，可無縫串接 macOS 內建的 `cron` 服務實現定時任務（Cron Job）。

---

## 🏗️ 系統架構與資料流 (System Architecture)


```

[ X 平台原始貼文 ]
│
▼ (scraper.py: Playwright 自動化擷取)
[ raw_tweets.json ]
│
▼ (parser.py: Gemini 2.5 Flash 結構化解析)
[ parsed_tweets.json ]
│
▼ (db_setup.py: SQLite 數據持久化與去重)
[ serenity.db ]
│
▼ (build_site.py: 資料聚合與模板編譯)
[ index.html (最終互動儀表板) ]

```

---

## 📂 專案目錄結構

```text
serenity-tracker/
├── .env                  # 關鍵隱私憑證與 API 金鑰 (Git 已忽略)
├── .gitignore            # Git 版本控制忽略清單
├── README.md             # 專案說明文件
├── requirements.txt      # Python 相依套件清單
├── run_pipeline.sh       # 管線一鍵執行與日誌輸出腳本
├── scraper.py            # Playwright 網頁自動化爬蟲
├── parser.py             # Gemini API 文字結構化解析腳本
├── db_setup.py           # SQLite 資料庫初始化與寫入腳本
├── build_site.py         # 數據聚合與 HTML 靜態網頁生成器
├── template.html         # 前端儀表板 UI 骨架與樣式設計
└── index.html            # 最終生成的公開動態網頁 (由腳本自動產出)

```

---

## 🚀 快速開始 (Quick Start)

### 1. 環境建置

克隆專案並進入工作目錄：

```bash
git clone [https://github.com/your-username/serenity-watch.git](https://github.com/your-username/serenity-watch.git)
cd serenity-watch

```

建立並啟動 Python 虛擬環境：

```bash
# macOS / Linux
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate

```

安裝依賴套件並初始化 Playwright 瀏覽器核心：

```bash
pip install -r requirements.txt
playwright install

```

### 2. 配置環境變數 (`.env`)

在專案根目錄下建立 `.env` 檔案，填入以下必要憑證：

```env
# Google AI Studio 申請的 API 金鑰
GEMINI_API_KEY=your_gemini_api_key_here

# X 平台的登入 Session Cookie
X_AUTH_TOKEN=your_x_auth_token_here

```

> 💡 **如何獲取 `X_AUTH_TOKEN`？**
> 1. 使用電腦瀏覽器登入 X (Twitter) 帳號。
> 2. 按下 `F12`（或右鍵點擊「檢查」）開啟開發者工具。
> 3. 切換至 **Application (應用程式)** 標籤頁，在左側選單點開 **Cookies** -> `https://x.com`。
> 4. 在列表中找到名稱為 **`auth_token`** 的項目，複製其整串 Value 填入變數。
> 
> 

### 3. 運行資料管線

你可以透過執行整合 Shell 腳本來一鍵跑完完整的資料流：

```bash
chmod +x run_pipeline.sh
./run_pipeline.sh

```

管線執行成功後，目錄下會更新 `index.html`。你可以直接在 Mac 雙擊 `index.html` 透過任何瀏覽器檢視視覺化儀表板。

---

## ⏰ 自動化定時排程 (macOS Cron 設定)

若要實現全自動每小時背景更新，可利用系統內建的 `cron` 服務。

1. 在終端機輸入：
```bash
crontab -e

```


2. 進入編輯器後，寫入以下設定（設定在每小時的第 0 分鐘執行並輸出日誌）：
```text
0 * * * * /Users/your_username/serenity-tracker/run_pipeline.sh >> /Users/your_username/serenity-tracker/pipeline.log 2>&1

```


*(請將路徑中的 `your_username` 修改為你實際的 Mac 使用者名稱)*

---

## 🗺️ 開發路線圖 (Roadmap)

* [x] 基礎架構從動態伺服器轉型為全靜態網站生成 (SSG)
* [x] 本地端數據去重與 Ticker 級別的多維度歸戶
* [ ] 整合 **GitHub Actions** 實現雲端無人值守自動化抓取
* [ ] 引入動態報價 API（如 Yahoo Finance）計算觀點發布後的個股累計報酬率（Alpha 追蹤）
* [ ] 實作 週/月/季 的提及頻率與市場情緒推移排行榜

---

## ⚠️ 免責聲明 (Disclaimer)

本專案僅供技術學術研究與資訊聚合展示之用。
網頁中呈現的情緒標籤（多頭/空頭/中立）與觀點摘要皆由大語言模型（LLM）自動解讀與推論生成，系統不保證其 100% 的準確性與時效性。**本專案所有內容均不構成任何形式的投資建議或操作指引。** 投資人進行決策前，請務必點擊詳情連結檢視原文，並進行獨立研究與風險評估。