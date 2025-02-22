from datetime import datetime
from xml.etree import ElementTree as ET

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
        root = ET.fromstring(xml_content)
        urls = []
        for url in root.findall(".//url"):
            loc = url.get("loc")

            temp_last_modified = url.get("lastmod")
            if temp_last_modified:
                last_modified = datetime.fromisoformat(temp_last_modified)
            else:
                last_modified = None

            change_frequency = url.get("changefreq")

            temp_priority = url.get("priority")
            if temp_priority:
                priority = float(temp_priority)
            else:
                priority = None

            urls.append(
                SitemapUrl(
                    loc=loc,
                    last_modified=last_modified,
                    change_frequency=change_frequency,
                    priority=priority,
                )
            )
        return urls
