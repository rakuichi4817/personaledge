import requests

from ..domains.models import SitemapUrl
from ..domains.services import SitemapDomainService


class WebPageService:
    """Webページを扱うアプリケーションサービス"""

    def fetch_sitemap(self, url: str) -> list[SitemapUrl]:
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
        return SitemapDomainService.parse(response.text)
