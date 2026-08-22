import os
import requests
from bs4 import BeautifulSoup

# 環境変数から Discord Webhook URL を取得
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

# Apple認定整備済製品 Mac一覧ページ
TARGET_URL = "https://www.apple.com/jp/shop/refurbished/mac"

def send_discord_notify(message):
    if not DISCORD_WEBHOOK_URL:
        print("Webhook URLが設定されていません。")
        return
    data = {"content": message}
    requests.post(DISCORD_WEBHOOK_URL, json=data)

def check_stock():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }
    response = requests.get(TARGET_URL, headers=headers)
    
    if response.status_code != 200:
        print(f"ページ取得失敗: HTTP {response.status_code}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    page_text = soup.get_text()

    # 条件判定：「Mac mini」「M4 Pro」「64GB」を含み、かつ「1TB」以上のSSD条件を満たすか
    has_mac_mini = "Mac mini" in page_text
    has_m4_pro = "M4 Pro" in page_text
    has_64gb = "64GB" in page_text
    
    # 1TB, 2TB, 4TB, 8TB のいずれかが含まれているか判定
    has_target_storage = any(storage in page_text for storage in ["1TB", "2TB", "4TB", "8TB"])

    if has_mac_mini and has_m4_pro and has_64gb and has_target_storage:
        msg = f"🚨 **【入荷検知】Mac mini (M4 Pro / 64GB / 1TB以上) の整備済製品が出ました！**\n{TARGET_URL}"
        send_discord_notify(msg)
        print("条件合致：通知を送信しました。")
    else:
        print("該当商品なし。")

if __name__ == "__main__":
    check_stock()
