import sqlite3

DB_PATH = "monitor.db"

def init_db():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            keyword TEXT NOT NULL,
            platforms TEXT NOT NULL DEFAULT 'reddit,hackernews',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(email, keyword)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS sent_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL UNIQUE,
            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 给旧数据加platforms字段（如果没有的话）
    try:
        cur.execute("ALTER TABLE subscriptions ADD COLUMN platforms TEXT NOT NULL DEFAULT 'reddit,hackernews'")
    except:
        pass

    con.commit()
    con.close()

def add_subscription(email, keyword, platforms="reddit,hackernews"):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    try:
        cur.execute(
            "INSERT INTO subscriptions (email, keyword, platforms) VALUES (?, ?, ?)",
            (email, keyword, platforms)
        )
        con.commit()
        print(f"✅ 已添加订阅: {email} 监控 '{keyword}' 在 {platforms}")
    except sqlite3.IntegrityError:
        # 更新platforms
        cur.execute(
            "UPDATE subscriptions SET platforms=? WHERE email=? AND keyword=?",
            (platforms, email, keyword)
        )
        con.commit()
        print(f"⚠️  已更新订阅: {email} '{keyword}' 的平台设置")
    finally:
        con.close()

def get_all_subscriptions():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT email, keyword, platforms FROM subscriptions")
    rows = cur.fetchall()
    con.close()
    return rows

def is_already_sent(url):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT 1 FROM sent_items WHERE url = ?", (url,))
    result = cur.fetchone()
    con.close()
    return result is not None

def mark_as_sent(url):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    try:
        cur.execute("INSERT INTO sent_items (url) VALUES (?)", (url,))
        con.commit()
    except sqlite3.IntegrityError:
        pass
    finally:
        con.close()