#!/bin/bash
cd /Users/roger/serenity-tracker
source venv/bin/activate
echo "=== 執行時間：$(date) ==="
python scraper.py
python parser.py
python db_setup.py
python build_site.py  # 新增此行：產出最新 index.html
echo "=== 執行結束 ==="