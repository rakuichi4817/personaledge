from datetime import datetime

from pydantic import AnyHttpUrl

from personaledge.domains.models import SitemapPage
from personaledge.domains.services import WebPageDomainService


class TestWebPageDomainService:
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
        result = WebPageDomainService.parse_sitemap(sitemap)

        # THEN: サイトマップが正しくパースされている
        expected_urls = [
            SitemapPage(
                loc=AnyHttpUrl("https://example.com"),
                last_modified=datetime(2021, 1, 1),
                change_frequency="daily",
                priority=0.8,
            ),
            SitemapPage(
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

    def test_parse_web_page_ページを正しく取得できる(self):
        # GIVEN: GoogleページのURL
        url = AnyHttpUrl("https://rakuichi4817.github.io/")
        html_text = """
        <!DOCTYPE html>
        <html lang="ja">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>テストダヨーン</title>
        </head>
        <body>
            <h1>テストダヨーン</h1>
            <p>これはテスト用のシンプルなHTMLファイルです。</p>
        </body>
        </html>
        """

        # WHEN: Googleページを取得
        result = WebPageDomainService.parse_web_page(html_text=html_text, url=url)

        # THEN: Googleページが正しく取得されている
        assert result.url == AnyHttpUrl(url)
        assert result.title == "テストダヨーン"
        assert "テストダヨーン" in result.content

    def test_filter_pages_指定日以降のページを取得できる(self):
        # GIVEN: テストサイトマップがある
        pages = [
            SitemapPage(
                loc=AnyHttpUrl("https://example.com"),
                last_modified=datetime(2021, 1, 1, 0, 0, 0),
                change_frequency="daily",
                priority=0.8,
            ),
            SitemapPage(
                loc=AnyHttpUrl("https://example.com/1"),
                last_modified=datetime(2021, 1, 2, 0, 0, 0),
                change_frequency=None,
                priority=None,
            ),
            SitemapPage(
                loc=AnyHttpUrl("https://example.com/2"),
                last_modified=datetime(2021, 1, 3, 0, 0, 0),
                change_frequency=None,
                priority=None,
            ),
        ]

        # WHEN: 指定日以降のページを取得
        result = WebPageDomainService.filter_pages(
            pages, from_datetime=datetime(2021, 1, 2, 0, 0, 0)
        )

        # THEN: 指定日以降のページが取得されている
        assert len(result) == 2
        assert result[0].loc == AnyHttpUrl("https://example.com/1")
        assert result[1].loc == AnyHttpUrl("https://example.com/2")

    def test_filter_pages_指定したURLから始まるページを正しく取得できる(self):
        # GIVEN: テストサイトマップがある
        pages = [
            SitemapPage(
                loc=AnyHttpUrl("https://example.com"),
                last_modified=datetime(2021, 1, 1, 0, 0, 0),
                change_frequency="daily",
                priority=0.8,
            ),
            SitemapPage(
                loc=AnyHttpUrl("https://example.com/posts/1"),
                last_modified=datetime(2021, 1, 2, 0, 0, 0),
                change_frequency=None,
                priority=None,
            ),
            SitemapPage(
                loc=AnyHttpUrl("https://example.com/posts/2"),
                last_modified=datetime(2021, 1, 3, 0, 0, 0),
                change_frequency=None,
                priority=None,
            ),
        ]

        # WHEN: 指定したURLから始まるページを取得
        result = WebPageDomainService.filter_pages(
            pages, url_prefix="https://example.com/posts/"
        )

        # THEN: 指定したURLから始まるページが取得されている
        assert len(result) == 2
        assert result[0].loc == AnyHttpUrl("https://example.com/posts/1")
        assert result[1].loc == AnyHttpUrl("https://example.com/posts/2")

    def test_filter_pages_指定した時間までのページ一覧を取得できる(self):
        # GIVEN: テストサイトマップがある
        pages = [
            SitemapPage(
                loc=AnyHttpUrl("https://example.com"),
                last_modified=datetime(2021, 1, 1, 0, 0, 0),
                change_frequency="daily",
                priority=0.8,
            ),
            SitemapPage(
                loc=AnyHttpUrl("https://example.com/posts/1"),
                last_modified=datetime(2021, 1, 2, 0, 0, 0),
                change_frequency=None,
                priority=None,
            ),
            SitemapPage(
                loc=AnyHttpUrl("https://example.com/posts/2"),
                last_modified=datetime(2021, 1, 3, 0, 0, 0),
                change_frequency=None,
                priority=None,
            ),
        ]

        # WHEN: 指定した時間までのページ一覧を取得
        result = WebPageDomainService.filter_pages(
            pages, to_datetime=datetime(2021, 1, 2, 12, 0, 0)
        )

        # THEN: 指定した時間までのページ一覧が取得されている
        assert len(result) == 2
        assert result[0].loc == AnyHttpUrl("https://example.com")
        assert result[1].loc == AnyHttpUrl("https://example.com/posts/1")

    def test_filter_pages_指定したURLから始まり指定範囲のページを正しく取得できる(self):
        # GIVEN: テストサイトマップがある
        pages = [
            SitemapPage(
                loc=AnyHttpUrl("https://example.com"),
                last_modified=datetime(2021, 1, 1, 0, 0, 0),
                change_frequency="daily",
                priority=0.8,
            ),
            SitemapPage(
                loc=AnyHttpUrl("https://example.com/posts/1"),
                last_modified=datetime(2021, 1, 2, 0, 0, 0),
                change_frequency=None,
                priority=None,
            ),
            SitemapPage(
                loc=AnyHttpUrl("https://example.com/posts/2"),
                last_modified=datetime(2021, 1, 3, 0, 0, 0),
                change_frequency=None,
                priority=None,
            ),
            SitemapPage(
                loc=AnyHttpUrl("https://example.com/2"),
                last_modified=datetime(2021, 1, 3, 0, 0, 0),
                change_frequency=None,
                priority=None,
            ),
        ]

        # WHEN: 指定したURLから始まり指定範囲のページを取得
        result = WebPageDomainService.filter_pages(
            pages,
            url_prefix="https://example.com/posts/",
            from_datetime=datetime(2021, 1, 3, 0, 0, 0),
            to_datetime=datetime(2021, 1, 4, 0, 0, 0),
        )

        # THEN: 指定したURLから始まり指定範囲のページが取得されている
        assert len(result) == 1
        assert result[0].loc == AnyHttpUrl("https://example.com/posts/2")
