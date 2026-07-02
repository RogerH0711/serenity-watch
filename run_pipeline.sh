#!/bin/bash

# 1. 切換至專案絕對路徑
cd /Users/roger/serenity-tracker

# 2. 啟動虛擬環境
source venv/bin/activate

# 3. 依序執行工作管線，並記錄執行時間
echo "=== 執行時間：$(date) ==="
python scraper.py
python parser.py
python db_setup.py
echo "=== 執行結束 ==="
