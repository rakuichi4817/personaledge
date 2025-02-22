from personaledge.domains.services import SitemapDomainService


class TestSitemapDomainService:
    def test_正しくサイトマップのパースができる(self):
        # GIVEN: テストサイトマップがある
        sitemap = """
        <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
            <url>
                <loc>https://example.com</loc>
                <lastmod>2021-01-01</lastmod>
                <changefreq>daily</changefreq>
                <priority>0.8</priority>
            </url>
            <url>
                <loc>https://example.com/1</loc>
                <lastmod>2021-01-02</lastmod>
            </url>
        </urlset>
        """

        # WHEN: サイトマップをパース
        result = SitemapDomainService.parse(sitemap)

        # THEN: サイトマップが正しくパースされている
        expected_urls = [
            {
                "loc": "https://example.com",
                "last_modified": (2021, 1, 1),
                "change_frequency": "daily",
                "priority": 0.8,
            },
            {
                "loc": "https://example.com/1",
                "last_modified": (2021, 1, 2),
                "change_frequency": None,
                "priority": None,
            },
        ]

        for i, url in enumerate(result):
            expected_url = expected_urls[i]
            assert url.loc == expected_url["loc"]
            assert (
                url.last_modified.year,
                url.last_modified.month,
                url.last_modified.day,
            ) == expected_url["last_modified"]
            assert url.change_frequency == expected_url["change_frequency"]
            assert url.priority == expected_url["priority"]
