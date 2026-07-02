# Serenity Watch

Automated opinion tracker and RAG system for specific X (Twitter) accounts. 

## 系統架構
* **Data Ingestion**: Playwright
* **Data Structuring**: Google Gemini-2.5-flash API
* **Database**: SQLite
* **Frontend & RAG**: Streamlit

## 本機端啟動指南
1. 安裝環境：`pip install -r requirements.txt` (與 Playwright: `playwright install`)
2. 建立 `.env` 檔案並設定 `GEMINI_API_KEY`
3. 執行爬蟲與資料庫建立：`./run_pipeline.sh`
4. 啟動前端：`streamlit run app.py`