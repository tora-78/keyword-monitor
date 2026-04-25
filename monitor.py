from scraper import fetch_hn, fetch_reddit, fetch_devto
from database import init_db, get_all_subscriptions, is_already_sent, mark_as_sent
from mailer import send_alert

PLATFORM_FETCHERS = {
    "reddit": fetch_reddit,
    "hackernews": fetch_hn,
    "devto": fetch_devto,
}

def run():
    init_db()
    subscriptions = get_all_subscriptions()

    if not subscriptions:
        print("⚠️  没有任何订阅")
        return

    # 按关键词+平台组合分组
    keyword_map = {}
    for email, keyword, platforms in subscriptions:
        key = (keyword, platforms)
        keyword_map.setdefault(key, []).append(email)

    for (keyword, platforms_str), emails in keyword_map.items():
        platform_list = [p.strip() for p in platforms_str.split(",")]
        
        results = []
        for platform in platform_list:
            fetcher = PLATFORM_FETCHERS.get(platform)
            if fetcher:
                print(f"\n🔍 搜索 {platform}: {keyword}")
                results += fetcher(keyword)

        # 过滤已发送
        new_results = [r for r in results if not is_already_sent(r["url"])]

        if not new_results:
            print(f"  没有新内容，跳过。")
            continue

        for email in emails:
            send_alert(email, keyword, new_results)

        for r in new_results:
            mark_as_sent(r["url"])

if __name__ == "__main__":
    run()