from scraper import search_all
from database import init_db, get_all_subscriptions, is_already_sent, mark_as_sent
from mailer import send_alert

def run():
    init_db()
    subscriptions = get_all_subscriptions()

    if not subscriptions:
        print("⚠️  没有任何订阅，请先添加。")
        return

    # 按关键词分组，避免同一关键词搜索多次
    keyword_map = {}
    for email, keyword in subscriptions:
        keyword_map.setdefault(keyword, []).append(email)

    for keyword, emails in keyword_map.items():
        results = search_all(keyword)

        # 过滤掉已经发送过的
        new_results = [r for r in results if not is_already_sent(r["url"])]

        if not new_results:
            print(f"  '{keyword}' 没有新内容，跳过。")
            continue

        # 给每个订阅该关键词的用户发邮件
        for email in emails:
            send_alert(email, keyword, new_results)

        # 标记为已发送
        for r in new_results:
            mark_as_sent(r["url"])

if __name__ == "__main__":
    run()