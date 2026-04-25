import resend
import os
from dotenv import load_dotenv

load_dotenv()
resend.api_key = os.getenv("RESEND_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL")

def send_alert(to_email, keyword, results):
    """发送关键词提醒邮件"""
    if not results:
        return

    # 拼装邮件内容
    items_html = ""
    for r in results:
        items_html += f"""
        <div style="margin-bottom:16px; padding:12px; border-left:3px solid #4F46E5;">
            <a href="{r['url']}" style="font-size:15px; color:#4F46E5; text-decoration:none;">
                {r['title']}
            </a>
            <p style="margin:4px 0 0; color:#666; font-size:13px;">
                {r['source']} · by {r['author']}
            </p>
        </div>
        """

    html = f"""
    <div style="font-family:sans-serif; max-width:600px; margin:0 auto;">
        <h2 style="color:#1a1a1a;">🔔 关键词提醒：<em>{keyword}</em></h2>
        <p style="color:#444;">发现 {len(results)} 条新内容：</p>
        {items_html}
        <hr style="border:none; border-top:1px solid #eee; margin:24px 0;">
        <p style="color:#999; font-size:12px;">
            你收到此邮件是因为你订阅了关键词监控服务。
        </p>
    </div>
    """

    params = {
        "from": FROM_EMAIL,
        "to": [to_email],
        "subject": f"[关键词监控] 发现关于 '{keyword}' 的新内容",
        "html": html,
    }

    resend.Emails.send(params)
    print(f"✅ 邮件已发送至 {to_email}")


if __name__ == "__main__":
    # 测试发送
    test_results = [
        {
            "source": "Reddit",
            "title": "How I made $1000 as a solopreneur",
            "url": "https://reddit.com/r/test",
            "author": "testuser",
        }
    ]
    send_alert("xherojp@gmail.com", "solopreneur", test_results)