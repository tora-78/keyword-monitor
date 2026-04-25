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
    platforms = data.get("platforms", "reddit,hackernews").strip()

    if not email or not keywords:
        return jsonify({"error": "Email and keywords are required"}), 400

    if not platforms:
        return jsonify({"error": "Please select at least one platform"}), 400

    keyword_list = [k.strip() for k in keywords.split(",") if k.strip()]

    for keyword in keyword_list:
        add_subscription(email, keyword, platforms)

    return jsonify({"success": True, "message": f"Subscribed to {len(keyword_list)} keyword(s)"})

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
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)