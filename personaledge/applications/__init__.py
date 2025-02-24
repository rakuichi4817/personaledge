import time
from collections.abc import Generator
from datetime import datetime, timedelta

import requests
from pydantic import AnyHttpUrl

from ..domains.models import PersonalizedWebPageContent, SitemapPage
from ..domains.services import PersonalizeDomainService, WebPageDomainService
from ..logger import get_logger

logger = get_logger(__name__)


class AppService:
    """アプリケーションサービス層

    NOTE: 処理が肥大化したらファイルを分ける
    """

    def __init__(
        self,
        personalize_domain_service: PersonalizeDomainService,
        web_page_domain_service: WebPageDomainService,
    ):
        self.personalize_domain_service = personalize_domain_service
        self.web_page_domain_service = web_page_domain_service

    def fetch_sitemap(self, url: str) -> list[SitemapPage]:
        """サイトマップを取得してパース

        Notes:
            データの永続化は現状行わない

        Args:
            url (str): サイトマップのURL

        Returns:
            list[SitemapUrl]: サイトマップのURLリスト
        """
        response = requests.get(url)
        response.raise_for_status()
        return self.web_page_domain_service.parse_sitemap(response.text)

    def fetch_and_personalize_web_page(
        self, url: str, prompty_filepath: str, interest: str
    ) -> PersonalizedWebPageContent:
        """Webページを取得して個人最適化

        Args:
            url (str): 対象のWebページのURL
            prompty_filepath (str): promptyファイルのパス
            interest (str): 個人最適化のための興味関心事項

        Returns:
            PersonalizedWebPageContent: 個人最適化されたWebページのコンテンツ情報
        """
        logger.info(f"Webページの取得: {url}")
        response = requests.get(url)
        response.raise_for_status()

        logger.info(f"Webページのパース: {url}")
        web_page_content = self.web_page_domain_service.parse_web_page(
            response.text, AnyHttpUrl(url)
        )

        logger.info(f"Webページの個人最適化: {url}")
        return self.personalize_domain_service.personalize_content(
            prompty_filepath=prompty_filepath,
            web_page_content=web_page_content,
            interest=interest,
        )

    def fetch_and_personalize_latest_page_from_sitemap(
        self,
        url: str,
        prompty_filepath: str,
        interest: str,
        timedelta: timedelta = timedelta(days=1),
        url_prefix: str | None = None,
        sleep_time: int = 1,
    ) -> Generator[PersonalizedWebPageContent, None, None]:
        """サイトマップから最新のページを取得して個人最適化

        Args:
            url (str): サイトマップのURL
            prompty_filepath (str): promptyファイルのパス
            interest (str): 個人最適化のための興味関心事項
            timedelta (timedelta): 指定範囲の時間 default: 1日
            url_prefix (str | None): URLのプレフィックス default: None

        Returns:
            Generator[PersonalizedWebPageContent, None, None]: 個人最適化されたWebページのコンテンツ情報
        """
        logger.info(f"サイトマップの取得: {url}")
        response = requests.get(url)
        response.raise_for_status()
        sitemap_pages = self.web_page_domain_service.parse_sitemap(response.text)

        logger.info("指定範囲のページをフィルターします")
        now = datetime.now()
        from_datetime = now - timedelta
        logger.info(f"次の時間以降に更新されたページを取得します: {from_datetime}")
        if url_prefix:
            logger.info(f"URLのプレフィックス: {url_prefix})")

        filtered_sitemap_pages = self.web_page_domain_service.filter_pages(
            sitemap_pages=sitemap_pages,
            from_datetime=from_datetime,
            url_prefix=url_prefix,
        )
        logger.info(f"対象のページ一覧: {filtered_sitemap_pages}")

        logger.info(f"「{interest}」で個人最適化を行います")

        for page in filtered_sitemap_pages:
            personalized_web_page = self.fetch_and_personalize_web_page(
                url=page.loc, prompty_filepath=prompty_filepath, interest=interest
            )
            time.sleep(sleep_time)
            yield personalized_web_page


def get_app_service() -> AppService:
    """AppServiceのインスタンスを取得

    Returns:
        AppService: AppServiceのインスタンス
    """
    return AppService(
        personalize_domain_service=PersonalizeDomainService(),
        web_page_domain_service=WebPageDomainService(),
    )
