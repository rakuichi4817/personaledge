import json
import sys

import requests

from personaledge.applications import get_app_service
from personaledge.logger import get_logger

logger = get_logger(__name__)


def send_slack_notification(webhook_url: str, message: str):
    """
    Slackに通知を送る関数
    :param webhook_url: SlackのIncoming Webhook URL
    :param message: 送信するメッセージ
    """
    payload = {"text": message}
    headers = {"Content-Type": "application/json"}

    response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)

    if response.status_code == 200:
        print("通知が送信されました。")
    else:
        print(f"通知の送信に失敗しました: {response.status_code}, {response.text}")


def target_page_to_slack():
    # 引数の取得
    args = sys.argv[1:]

    # 引数の数が足りない場合はエラー
    if len(args) < 4:
        logger.error("引数が足りません")
        logger.error(
            "Usage: personaledge <URL> <PROMPTY_FILE> <INTEREST> <WEBHOOK_URL>"
        )
        sys.exit(1)

    # 引数の取得
    url = args[0]
    prompty_filepath = args[1]
    interest = args[2]
    webhook_url = args[3]

    # アプリケーションサービスの取得
    app_service = get_app_service()

    # Webページの取得と個人最適化
    personalized_web_page_content = app_service.fetch_and_personalize_web_page(
        url=url, prompty_filepath=prompty_filepath, interest=interest
    )

    # 結果の出力
    logger.info(f"URL: {personalized_web_page_content.url}")
    logger.info(f"Title: {personalized_web_page_content.title}")
    logger.info(f"Interest: {personalized_web_page_content.interest}")
    logger.info(
        f"personalized_content: {personalized_web_page_content.personalized_content}"
    )

    # Slackに通知
    message = f"{personalized_web_page_content.personalized_content}\n\n■URL: <{personalized_web_page_content.url}>\n■Title: {personalized_web_page_content.title}"
    send_slack_notification(webhook_url, message)


if __name__ == "__main__":
    target_page_to_slack()
