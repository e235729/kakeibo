import sqlite3
from datetime import datetime

# データベースに接続
conn = sqlite3.connect('financial_management.db')
cursor = conn.cursor()

# テーブル「取引情報 DB」を作成
cursor.execute('''
CREATE TABLE IF NOT EXISTS Transaction (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_type TEXT CHECK(transaction_type IN ('収入', '支出')) NOT NULL,
    amount INTEGER NOT NULL,
    date TEXT NOT NULL,
    memo_id INTEGER,
    message_id INTEGER,
    FOREIGN KEY (memo_id) REFERENCES Memo(memo_id),
    FOREIGN KEY (message_id) REFERENCES Message(message_id)
)
''')

# テーブル「メモ情報 DB」を作成
cursor.execute('''
CREATE TABLE IF NOT EXISTS Memo (
    memo_id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
)
''')

# テーブル「メッセージ情報 DB」を作成
cursor.execute('''
CREATE TABLE IF NOT EXISTS Message (
    message_id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    type TEXT CHECK(type IN ('通知', 'リマインダー')) NOT NULL
)
''')

# サンプルデータを挿入（必要に応じて）
cursor.execute('''
INSERT INTO Memo (content, created_at, updated_at) VALUES 
('初期メモ', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
''')

cursor.execute('''
INSERT INTO Message (content, created_at, type) VALUES 
('初期メッセージ', CURRENT_TIMESTAMP, '通知')
''')

# 変更を保存
conn.commit()

# データベース接続を閉じる
conn.close()
