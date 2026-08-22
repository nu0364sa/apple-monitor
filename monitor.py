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

    # ★★★ ここがテスト用条件（ページ内にある「Mac」という文字だけで無条件ヒット） ★★★
    has_mac_mini = "Mac" in page_text
    has_m4_pro = True
    has_64gb = True
    has_target_storage = True

    if has_mac_mini and has_m4_pro and has_64gb and has_target_storage:
        msg = f"🚨 **【テスト通知】Discordへの通知テストです！動作OK！**\n{TARGET_URL}"
        send_discord_notify(msg)
        print("条件合致：通知を送信しました。")
    else:
        print("該当商品なし。")

if __name__ == "__main__":
    check_stock()
