from flask import Flask, request, jsonify, send_from_directory
from database import init_db, add_subscription, get_all_subscriptions
import os

app = Flask(__name__)

@app.route("/")
def index():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), "index.html")

@app.route("/subscribe", methods=["POST"])
def subscribe():
    data = request.get_json()
    email = data.get("email", "").strip()
    keywords = data.get("keywords", "").strip()

    if not email or not keywords:
        return jsonify({"error": "邮箱和关键词不能为空"}), 400

    # 支持多个关键词，用逗号分隔
    keyword_list = [k.strip() for k in keywords.split(",") if k.strip()]

    for keyword in keyword_list:
        add_subscription(email, keyword)

    return jsonify({"success": True, "message": f"成功订阅 {len(keyword_list)} 个关键词"})

@app.route("/subscriptions", methods=["GET"])
def subscriptions():
    email = request.args.get("email", "")
    all_subs = get_all_subscriptions()
    if email:
        result = [{"email": e, "keyword": k} for e, k in all_subs if e == email]
    else:
        result = [{"email": e, "keyword": k} for e, k in all_subs]
    return jsonify(result)

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)