from datetime import datetime

from pydantic import AnyHttpUrl

from personaledge.domains.models import SitemapUrl
from personaledge.domains.services import SitemapDomainService


class TestSitemapDomainService:
    def test_正しくサイトマップのパースができる(self):
        # GIVEN: テストサイトマップがある
        sitemap = """
        <?xml version="1.0" encoding="utf-8" standalone="yes"?>
        <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">
            <url>
                <loc>https://example.com</loc>
                <lastmod>2025-02-01T00:00:00+00:00</lastmod>
                <changefreq>daily</changefreq>
                <priority>0.8</priority>
            </url>
            <url>
                <loc>https://example.com/1</loc>
                <lastmod>2025-02-02T00:00:00+00:00</lastmod>
            </url>
        </urlset>
        """

        # WHEN: サイトマップをパース
        result = SitemapDomainService.parse(sitemap)

        # THEN: サイトマップが正しくパースされている
        expected_urls = [
            SitemapUrl(
                loc=AnyHttpUrl("https://example.com"),
                last_modified=datetime(2021, 1, 1),
                change_frequency="daily",
                priority=0.8,
            ),
            SitemapUrl(
                loc=AnyHttpUrl("https://example.com/1"),
                last_modified=datetime(2021, 1, 2),
                change_frequency=None,
                priority=None,
            ),
        ]

        for i, url in enumerate(result):
            expected_url = expected_urls[i]
            assert url.loc == expected_url.loc
            assert (
                url.last_modified.year,
                url.last_modified.month,
                url.last_modified.day,
            ) == expected_url.last_modified
            assert url.change_frequency == expected_url.change_frequency
            assert url.priority == expected_url.priority
