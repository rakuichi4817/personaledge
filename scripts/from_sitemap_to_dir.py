import datetime
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from personaledge.applications import get_app_service
from personaledge.logger import get_logger

logger = get_logger(__name__)

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app_service = get_app_service()


def main():
    logger.info(
        "サイトマップから指定条件のURLを取得し、ディレクトリに最適化結果を保存するスクリプトです。"
    )

    logger.info(f"引数の取得: {sys.argv}")
    args = sys.argv[1:]

    # 引数の数が足りない場合はエラー
    if len(args) < 4:
        logger.error("引数が足りません")
        logger.error(
            "Usage: personaledge <SITEMAP_URL> <PROMPTY_FILE> <INTEREST> <OUTPUT_DIR> <URL_PREFIX> <TIMDELTA>"
        )
        sys.exit(1)

    sitemap_url = args[0]
    prompty_filepath = os.path.join(os.getcwd(), args[1])
    interest = args[2]
    output_dir = args[3]
    url_prefix = args[4] if args[4] != "skip" else None
    timedelta = int(args[5]) if len(args) > 5 else 1

    logger.info(
        f"引数情報: SITEMAP_URL={sitemap_url}, PROMPTY_FILE={prompty_filepath}, INTEREST={interest}, OUTPUT_DIR={output_dir}, URL_PREFIX={url_prefix}, TIMDELTA={timedelta}"
    )

    logger.info("出力先ディレクトリを作成します")
    os.makedirs(output_dir, exist_ok=True)

    logger.info("サイトマップから最新のページを取得して個人最適化を行います")
    personalized_pages = app_service.fetch_and_personalize_latest_page_from_sitemap(
        url=sitemap_url,
        prompty_filepath=prompty_filepath,
        interest=interest,
        timedelta=datetime.timedelta(timedelta),
        url_prefix=url_prefix,
        sleep_time=5,
    )
    for page in personalized_pages:
        logger.info(f"ページを取得しました: {page.title}")

        logger.info("個人最適化結果をファイルに保存します")
        output_filepath = os.path.join(root_path, output_dir, f"{page.title}.md")
        with open(output_filepath, "w") as f:
            f.write(page.personalized_content)
            f.write("\n\n---\n\n")
            f.write(f"【URL】 <{page.url}><br>\n")
            f.write(f"【Title】 {page.title}\n\n")
        logger.info(f"ファイルを保存しました: {output_filepath}")


if __name__ == "__main__":
    main()
