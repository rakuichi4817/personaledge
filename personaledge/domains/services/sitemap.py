from pydantic import AnyHttpUrl
from usp.tree import sitemap_from_str

from ..models.sitemap import SitemapUrl


class SitemapDomainService:
    """サイトマップ用のドメインサービス"""

    @staticmethod
    def parse(xml_content: str) -> list[SitemapUrl]:
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
                SitemapUrl(
                    loc=AnyHttpUrl(page.url),
                    last_modified=page.last_modified,
                    change_frequency=change_frequency,
                    priority=page.priority,
                )
            )
        return urls
