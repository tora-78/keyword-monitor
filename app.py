from flask import Flask, request, jsonify, send_from_directory, redirect
from database import init_db, add_subscription, get_all_subscriptions, count_subscriptions
from payments import create_checkout_session, is_paid_user
import os

app = Flask(__name__)

@app.route("/")
def index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.route("/subscribe", methods=["POST"])
def subscribe():
    data = request.get_json()
    email = data.get("email", "").strip()
    keywords = data.get("keywords", "").strip()
    platforms = data.get("platforms", "reddit,hackernews").strip()

    if not email or not keywords:
        return jsonify({"error": "Email and keywords are required"}), 400

    if not platforms:
        return jsonify({"error": "Please select at least one platform"}), 400

    keyword_list = [k.strip() for k in keywords.split(",") if k.strip()]

    # 检查免费用户总关键词数量
    if not is_paid_user(email):
        existing = count_subscriptions(email)
        if existing >= 1 or len(keyword_list) > 1:
            return jsonify({
                "error": "free_limit",
                "message": "Free plan allows 1 keyword only. Upgrade to Pro for unlimited keywords."
            }), 403

    for keyword in keyword_list:
        add_subscription(email, keyword, platforms)

    return jsonify({"success": True, "message": f"Subscribed to {len(keyword_list)} keyword(s)"})

@app.route("/checkout", methods=["POST"])
def checkout():
    data = request.get_json()
    email = data.get("email", "").strip()
    if not email:
        return jsonify({"error": "Email required"}), 400
    url = create_checkout_session(email)
    return jsonify({"url": url})

@app.route("/success")
def success():
    return """
    <html><body style="font-family:sans-serif;text-align:center;padding:80px">
    <h1>🎉 You're now a Pro member!</h1>
    <p>Go back and start monitoring unlimited keywords.</p>
    <a href="/" style="color:#4F46E5">← Back to Keyword Monitor</a>
    </body></html>
    """

@app.route("/cancel")
def cancel():
    return """
    <html><body style="font-family:sans-serif;text-align:center;padding:80px">
    <h1>Payment cancelled</h1>
    <p>No worries, you can upgrade anytime.</p>
    <a href="/" style="color:#4F46E5">← Back to Keyword Monitor</a>
    </body></html>
    """

@app.route("/subscriptions", methods=["GET"])
def subscriptions():
    email = request.args.get("email", "")
    all_subs = get_all_subscriptions()
    if email:
        result = [{"email": e, "keyword": k} for e, k, p in all_subs if e == email]
    else:
        result = [{"email": e, "keyword": k} for e, k, p in all_subs]
    return jsonify(result)

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

@app.route("/tokusho")
def tokusho():
    with open("tokusho.html", "r", encoding="utf-8") as f:
        return f.read()