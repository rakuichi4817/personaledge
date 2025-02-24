import os
from datetime import datetime

import pytest

from personaledge.applications import get_app_service
from personaledge.domains.models import PersonalizedWebPageContent, SitemapPage


class TestAppService:
    @pytest.fixture(autouse=True)
    def init_test(self, test_root_path) -> None:
        self.service = get_app_service()
        self.test_root_path = test_root_path

    def test_fetch_sitemap_正しくサイトマップが正しく取得できること(self):
        # GIVEN: テスト用サイトマップ
        url = "https://rakuichi4817.github.io/sitemap"

        # WHEN: サイトマップを取得
        result = self.service.fetch_sitemap(url)

        # THEN: サイトマップが正しく取得できている
        assert len(result) > 0
        assert all([url.loc for url in result])

    @pytest.mark.skipif(
        os.getenv("GITHUB_ACTIONS") == "true", reason="GitHub Actionsではスキップ"
    )
    def test_fetch_and_personalize_web_page_正しく個人最適化されたページを取得できること(
        self,
    ):
        # GIVEN: テスト用のWebページと興味トピックpromptyファイルパス
        url = "https://rakuichi4817.github.io/posts/2025/prompty-structured-outputs/"
        prompty_file = "sample.prompty"
        prompty_filepath = os.path.join(self.test_root_path, "data", prompty_file)
        interest = "スターウォーズ"

        # WHEN: サイトマップから最新のページを取得して個人最適化
        result = self.service.fetch_and_personalize_web_page(
            url, prompty_filepath, interest
        )

        # THEN: 個人最適化されたページが正しく取得できている
        assert str(result.url) == url
        assert "PromptyでStructured Outputsを使ってみる" in result.title
        assert result.interest == interest
        assert isinstance(result.generated_at, datetime)
        assert "Structured Outputs" in result.content

    @pytest.mark.skipif(
        os.getenv("GITHUB_ACTIONS") == "true", reason="GitHub Actionsではスキップ"
    )
    def test_fetch_and_personalize_latest_page_from_sitemap_正しくサイトマップから指定範囲内の個人最適化されたページを取得できること(
        self, mocker
    ):
        # GIVEN: テスト用のWebページと興味トピックpromptyファイルパス
        url = "https://rakuichi4817.github.io/sitemap"
        url_prefix = "https://rakuichi4817.github/posts/"
        prompty_file = "sample.prompty"
        prompty_filepath = os.path.join(self.test_root_path, "data", prompty_file)
        interest = "スターウォーズ"

        # リクエスト投げる部分のモック
        mocker.patch(
            "personaledge.domains.services.web_page.WebPageDomainService.filter_pages",
            return_value=[
                SitemapPage(
                    loc="https://rakuichi4817.github.io/posts/2025/prompty-structured-outputs/",
                ),
                SitemapPage(
                    loc="https://rakuichi4817.github.io/posts/2024/excalidraw-intro/",
                ),
            ],
        )

        mocker.patch(
            "personaledge.domains.services.personalize.PersonalizeDomainService.personalize_content",
            return_value=[
                PersonalizedWebPageContent(
                    url="https://rakuichi4817.github.io/posts/2025/prompty-structured-outputs/",
                    title="PromptyでStructured Outputsを使ってみる",
                    content="Structured Outputsを使ってみる",
                    interest="スターウォーズ",
                    generated_at=datetime.now(),
                    personalized_content="スターウォーズでStructured Outputsを例えた文章",
                ),
                PersonalizedWebPageContent(
                    url="https://rakuichi4817.github.io/posts/2024/excalidraw-intro/",
                    title="Excalidrawで図を描いてみる",
                    content="Excalidrawを使ってみる",
                    interest="スターウォーズ",
                    generated_at=datetime.now(),
                    personalized_content="スターウォーズでExcalidrawを例えた文章",
                ),
            ],
        )

        # WHEN: サイトマップから直近1日のページを取得して個人最適化
        result = self.service.fetch_and_personalize_latest_page_from_sitemap(
            url=url,
            prompty_filepath=prompty_filepath,
            interest=interest,
            url_prefix=url_prefix,
        )

        # THEN: 個人最適化されたページが正しく取得できている
        assert len(result) == 2
