"""
Threadsに投稿し、結果をログ(CSV)に記録するスクリプト。

将来的にはこのファイルが、GPT→Gemini→Claudeで生成した文章を受け取って
投稿する処理の中心になります。今の段階では、渡されたテキストをそのまま
投稿し、記録を残すところまでを実装しています。
"""

import os
import csv
import datetime
import requests
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("THREADS_ACCESS_TOKEN")
THREADS_USER_ID = os.getenv("THREADS_USER_ID")  # 自分のThreadsユーザーID
LOG_FILE = os.path.join(os.path.dirname(__file__), "logs", "post_log.csv")


def create_container(text: str) -> str:
    """投稿用のコンテナを作成し、container_idを返す"""
    url = f"https://graph.threads.net/v1.0/{THREADS_USER_ID}/threads"
    params = {
        "media_type": "TEXT",
        "text": text,
        "access_token": ACCESS_TOKEN,
    }
    resp = requests.post(url, params=params)
    resp.raise_for_status()
    return resp.json()["id"]


def publish_container(container_id: str) -> str:
    """作成済みコンテナを実際に投稿する"""
    url = f"https://graph.threads.net/v1.0/{THREADS_USER_ID}/threads_publish"
    params = {
        "creation_id": container_id,
        "access_token": ACCESS_TOKEN,
    }
    resp = requests.post(url, params=params)
    resp.raise_for_status()
    return resp.json()["id"]


def log_result(text: str, post_id: str, status: str, note: str = ""):
    """投稿結果をCSVに記録する（実績データとして蓄積）"""
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["日時", "投稿本文", "投稿ID", "ステータス", "備考"])
        writer.writerow(
            [datetime.datetime.now().isoformat(timespec="seconds"), text, post_id, status, note]
        )


def post_text(text: str):
    """テキストをThreadsに投稿し、ログに残す"""
    try:
        container_id = create_container(text)
        post_id = publish_container(container_id)
        log_result(text, post_id, "success")
        print(f"投稿成功: {post_id}")
        return post_id
    except Exception as e:
        log_result(text, "", "failed", str(e))
        print(f"投稿失敗: {e}")
        raise


if __name__ == "__main__":
    # 動作確認用のサンプル投稿
    sample_text = "これはThreads自動投稿システムのテスト投稿です。"
    post_text(sample_text)
