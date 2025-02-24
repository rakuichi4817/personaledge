from datetime import datetime

from bs4 import BeautifulSoup
from pydantic import AnyHttpUrl
from usp.tree import sitemap_from_str

from ...logger import get_logger
from ..models.page import WebPageContent
from ..models.sitemap import SitemapPage

logger = get_logger(__name__)


class WebPageDomainService:
    """Webページを扱うドメインサービス"""

    @staticmethod
    def parse_sitemap(xml_content: str) -> list[SitemapPage]:
        """xml_content をパースしてSitemapオブジェクトに変換

        Args:
            xml_content (str): サイトマップのXML文字列

        Returns:
            list[SitemapUrl]: サイトマップのURLリスト
        """
        tree = sitemap_from_str(xml_content)

        urls = []
        for page in tree.all_pages():
            if page.change_frequency:
                change_frequency = page.change_frequency.value
            else:
                change_frequency = None

            urls.append(
                SitemapPage(
                    loc=AnyHttpUrl(page.url),
                    last_modified=page.last_modified,
                    change_frequency=change_frequency,
                    priority=page.priority,
                )
            )
        return urls

    @staticmethod
    def parse_web_page(html_text: str, url: AnyHttpUrl) -> WebPageContent:
        """指定されたURLのWebページの内容を取得

        Args:
            html_text (str): 取得対象のWebページのURL
            url (AnyHttpUrl): 取得対象のWebページのURL

        Returns:
            WebPageContent: Webページのコンテンツ情報
        """
        # BeautifulSoupを使ってHTMLを解析
        soup = BeautifulSoup(html_text, "html.parser")

        # タイトルを取得（<title>タグを抽出）
        title = soup.title.string if soup.title else "No title found"

        # HTMLコンテンツを取得（bodyタグ内のコンテンツを抽出）
        content = str(soup.body) if soup.body else "No content found"

        # WebPageContentインスタンスを返す
        return WebPageContent(url=url, title=title, content=content)

    @staticmethod
    def filter_pages(
        pages: list[SitemapPage],
        url_prefix: str | None = None,
        from_datetime: datetime | None = None,
        to_datetime: datetime = datetime.now(),
    ) -> list[SitemapPage]:
        """指定された条件に基づいてページをフィルタリング

        Notes:
            以下条件
            - URLのプレフィックスが一致するページ
            - 指定時刻以降のページ: last_modified >= from_datetime
            - 指定時刻以前のページ

        Args:
            page_urls (list[SitemapPage]): サイトマップのURLリスト
            url_prefix (str | None): URLのプレフィックス default: None
            from_datetime (datetime | None): 指定時刻以降のページを取得 default: None
            to_datetime (datetime): 指定時刻以降のページを取得 default: datetime.now()

        Returns:
            list[SitemapUrl]: 更新されたページのURLリスト
        """
        urls = []
        for page in pages:
            if url_prefix and not str(page.loc).startswith(url_prefix):
                logger.info(f"URLのプレフィックスが一致しません: {page.loc}")
                continue
            if from_datetime or to_datetime:
                logger.info("時刻条件が指定されています")
                if page.last_modified is None:
                    logger.info(f"最終更新日時が取得できません: {page.loc}")
                    continue

                if from_datetime and page.last_modified < from_datetime:
                    logger.info(f"指定時刻以降のページではありません: {page.loc}")
                    continue
                if page.last_modified > to_datetime:
                    logger.info(f"指定時刻以前のページではありません: {page.loc}")
                    continue

            urls.append(page)

        return urls
