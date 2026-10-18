
import json
import logging
from datetime import datetime
from pathlib import Path
from urllib.request import Request, urlopen

from flask import Flask, request
from waitress import serve

BASE = Path(__file__).resolve().parent

with open(BASE / "config.json", encoding="utf-8") as f:
    config = json.load(f)

GROUPS = set(map(str, config["group_ids"]))
API = config["api_url"].rstrip("/")
TOKEN = config["access_token"]

app = Flask(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)


def send_message(group_id, text):
    payload = json.dumps({
        "group_id": int(group_id),
        "message": [
            {"type": "text", "data": {"text": text}}
        ]
    }).encode("utf-8")

    req = Request(
        f"{API}/send_group_msg",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {TOKEN}"
        },
        method="POST"
    )

    with urlopen(req, timeout=15) as response:
        result = json.load(response)

    if result.get("status") != "ok":
        raise RuntimeError(str(result))


@app.post("/event")
def receive_event():
    event = request.get_json(silent=True)

    if not isinstance(event, dict):
        return "Invalid JSON", 400

    if event.get("post_type") != "message":
        return "OK", 200

    if event.get("message_type") != "group":
        return "OK", 200

    group_id = str(event.get("group_id", ""))

    if group_id not in GROUPS:
        return "OK", 200

    # 避免机器人回复自己的消息
    sender_id = str(event.get("user_id", ""))
    self_id = str(event.get("self_id", ""))

    if sender_id == self_id:
        return "OK", 200

    message = event.get("raw_message", "").strip()

    if message == "/ping":
        reply = "pong 🏓 我还活着！"

    elif message == "/状态":
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        reply = f"机器人服务正常\n服务器时间：{now}"

    elif message == "/帮助":
        reply = (
            "【东东答机器人】\n"
            "/ping - 在线测试\n"
            "/状态 - 查看服务时间\n"
            "/帮助 - 查看命令"
        )

    else:
        return "OK", 200

    try:
        send_message(group_id, reply)
        app.logger.info("群 %s 回复成功", group_id)
    except Exception:
        app.logger.exception("发送回复失败")
        return "Send failed", 500

    return "OK", 200


if __name__ == "__main__":
    print("QQ 自动回复服务启动，监听 8080", flush=True)
    serve(app, host="172.18.0.1", port=8080, threads=4)
