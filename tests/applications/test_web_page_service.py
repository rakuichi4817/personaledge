import pytest

from personaledge.applications.web_page_service import WebPageService


class TestWebPageService:
    @pytest.fixture(autouse=True)
    def init_test(
        self,
    ) -> None:
        self.service = WebPageService()

    def test_fetch_sitemap_正しくサイトマップが正しく取得できること(self):
        # GIVEN: Googleのサイトマップ
        url = "https://rakuichi4817.github.io/sitemap"

        # WHEN: サイトマップを取得
        result = self.service.fetch_sitemap(url)

        # THEN: サイトマップが正しく取得できている
        assert len(result) > 0
        assert all([url.loc for url in result])
