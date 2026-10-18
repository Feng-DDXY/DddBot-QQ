import json
import time
import random
import urllib.request
from pathlib import Path

# 读取配置文件
BASE_DIR = Path(__file__).resolve().parent
config_path = BASE_DIR / "config.json"

with open(config_path, "r", encoding="utf-8") as f:
    config = json.load(f)

group_ids = config["group_ids"]
guagua_qq = str(config["guagua_qq"])
command = config["command"]
api_url = config["api_url"].rstrip("/")
token = config["access_token"]

# 向指定QQ群发送真正的@消息

for index, group_id in enumerate(group_ids):
    if index > 0:
        delay = random.randint(5, 15)
        print(f"等待 {delay} 秒后发送到群 {group_id}")
        time.sleep(delay)
    message = {
        "group_id": int(group_id),
        "message": [
            {
                "type": "at",
                "data": {"qq": guagua_qq}
            },
            {
                "type": "text",
                "data": {"text": " " + command}
            }
        ]
    }

    request = urllib.request.Request(
        url=f"{api_url}/send_group_msg",
        data=json.dumps(message).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            result = json.load(response)

        if result.get("status") == "ok":
            print(f"群 {group_id}：发送成功")
        else:
            print(f"群 {group_id}：发送失败，{result}")

    except Exception as e:
        print(f"群 {group_id}：请求异常，{e}")
