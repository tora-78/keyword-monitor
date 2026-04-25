import sqlite3

DB_PATH = "monitor.db"

def init_db():
    """初始化数据库，建表"""
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    # 用户关键词表
    cur.execute("""
        CREATE TABLE IF NOT EXISTS subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            keyword TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(email, keyword)
        )
    """)

    # 已发送记录表（防重复）
    cur.execute("""
        CREATE TABLE IF NOT EXISTS sent_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL UNIQUE,
            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    con.commit()
    con.close()
    print("✅ 数据库初始化完成")

def add_subscription(email, keyword):
    """添加一个监控订阅"""
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    try:
        cur.execute(
            "INSERT INTO subscriptions (email, keyword) VALUES (?, ?)",
            (email, keyword)
        )
        con.commit()
        print(f"✅ 已添加订阅: {email} 监控 '{keyword}'")
    except sqlite3.IntegrityError:
        print(f"⚠️  {email} 已经在监控 '{keyword}' 了")
    finally:
        con.close()

def get_all_subscriptions():
    """获取所有订阅"""
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT email, keyword FROM subscriptions")
    rows = cur.fetchall()
    con.close()
    return rows

def is_already_sent(url):
    """检查这个帖子是否已经发过提醒"""
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT 1 FROM sent_items WHERE url = ?", (url,))
    result = cur.fetchone()
    con.close()
    return result is not None

def mark_as_sent(url):
    """标记这个帖子已发送"""
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    try:
        cur.execute("INSERT INTO sent_items (url) VALUES (?)", (url,))
        con.commit()
    except sqlite3.IntegrityError:
        pass
    finally:
        con.close()

if __name__ == "__main__":
    init_db()
    # 测试添加订阅
    add_subscription("test@example.com", "solopreneur")
    add_subscription("test@example.com", "indie hacker")
    add_subscription("test@example.com", "solopreneur")  # 重复，应该提示
    
    print("\n当前所有订阅：")
    for email, keyword in get_all_subscriptions():
        print(f"  {email} → {keyword}")