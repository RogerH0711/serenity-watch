import sqlite3
import json
import os

DB_NAME = "serenity.db"

def init_db():
    # 連線至 SQLite 資料庫（若無檔案則自動建立）
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # 建立股票提及紀錄資料表 (mentions)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mentions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            ticker TEXT,
            sentiment TEXT,
            thesis TEXT,
            risks TEXT,
            url TEXT
        )
    ''')
    conn.commit()
    return conn, cursor

def load_data_to_db(conn, cursor):
    try:
        with open("parsed_tweets.json", "r", encoding="utf-8") as f:
            records = json.load(f)
    except FileNotFoundError:
        print("錯誤：找不到 parsed_tweets.json")
        return

    # 寫入資料庫
    inserted_count = 0
    for row in records:
        # 使用 INSERT OR IGNORE 避免重複插入相同網址與股票代碼的紀錄
        # 這裡為了簡單示範，直接插入。若要防止重複，可將 (url, ticker) 設為 UNIQUE
        cursor.execute('''
            INSERT INTO mentions (timestamp, ticker, sentiment, thesis, risks, url)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            row.get("timestamp"), 
            row.get("ticker"), 
            row.get("sentiment"), 
            row.get("thesis"), 
            row.get("risks"), 
            row.get("url")
        ))
        inserted_count += 1
    
    conn.commit()
    print(f"成功將 {inserted_count} 筆紀錄寫入 SQLite 資料庫 ({DB_NAME})")

if __name__ == "__main__":
    connection, db_cursor = init_db()
    load_data_to_db(connection, db_cursor)
    connection.close()