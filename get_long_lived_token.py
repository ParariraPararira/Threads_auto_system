"""
Threads APIの長期アクセストークンを取得するスクリプト。

使い方：
1. .env ファイルに THREADS_APP_ID と THREADS_APP_SECRET を書いておく
2. ブラウザで認証URLを開き、許可すると認証コード(code)が表示される
3. このスクリプトを実行し、コードを貼り付ける
4. 表示された長期トークンを .env の THREADS_ACCESS_TOKEN に保存する
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("THREADS_APP_ID")
APP_SECRET = os.getenv("THREADS_APP_SECRET")
REDIRECT_URI = os.getenv("THREADS_REDIRECT_URI")


def get_auth_url():
    return (
        "https://threads.net/oauth/authorize"
        f"?client_id={APP_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        "&scope=threads_basic,threads_content_publish"
        "&response_type=code"
    )


def exchange_code_for_short_token(code: str) -> str:
    url = "https://graph.threads.net/oauth/access_token"
    data = {
        "client_id": APP_ID,
        "client_secret": APP_SECRET,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
        "code": code,
    }
    resp = requests.post(url, data=data)
    resp.raise_for_status()
    return resp.json()["access_token"]


def exchange_short_for_long_token(short_token: str) -> dict:
    url = "https://graph.threads.net/access_token"
    params = {
        "grant_type": "th_exchange_token",
        "client_secret": APP_SECRET,
        "access_token": short_token,
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    return resp.json()


def get_user_id(access_token: str) -> str:
    url = "https://graph.threads.net/v1.0/me"
    params = {"fields": "id,username", "access_token": access_token}
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()
    print(f"アカウント: @{data.get('username', '不明')}")
    return data["id"]


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("=== Threads 長期アクセストークン取得 ===")
        print()
        print("以下のURLをブラウザで開いて認証コードを取得してください：")
        print(get_auth_url())
        print()
        print("使い方: python get_long_lived_token.py <認証コード>")
        sys.exit(1)

    code = sys.argv[1].strip()
    short_token = exchange_code_for_short_token(code)
    result = exchange_short_for_long_token(short_token)

    user_id = get_user_id(result["access_token"])

    print()
    print("取得成功！以下をリポジトリのSecretsに登録してください：")
    print(f"  THREADS_ACCESS_TOKEN = {result['access_token']}")
    print(f"  THREADS_USER_ID      = {user_id}")
    print(f"(トークンの有効期限: 約{result.get('expires_in', 0) // 86400}日)")
