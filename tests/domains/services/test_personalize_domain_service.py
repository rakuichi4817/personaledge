import os
from datetime import datetime

import pytest

from personaledge.domains.models import WebPageContent
from personaledge.domains.services import PersonalizeDomainService


class TestPersonalizeDomainService:
    @pytest.fixture(autouse=True)
    def init_test(self, test_root_path):
        self.service = PersonalizeDomainService()
        self.test_root_path = test_root_path

    def test__get_prompty_正しくPromptyの実行クライアントを作成できること(self):
        # GIVEN: Promptyファイルが存在するとき
        prompty_file = "sample.prompty"
        prompty_filepath = os.path.join(self.test_root_path, "data", prompty_file)

        # WHEN: Promptyファイルを与えて取得
        prompty = self.service._get_prompty(prompty_filepath)

        # THEN: 正しくPromptyの実行クライアントが作成されること
        assert prompty.model.configuration["type"] == "azure_openai"

    @pytest.mark.skipif(
        os.getenv("GITHUB_ACTIONS") == "true", reason="GitHub Actionsではスキップ"
    )
    def test_personalize_content_正しく個人最適化されたコンテンツを返すこと(self):
        # GIVEN: Promptyファイルとコンテンツが与えられたとき
        prompty_file = "sample.prompty"
        prompty_filepath = os.path.join(self.test_root_path, "data", prompty_file)
        content = "ChatGPTは、OpenAI社が独自に開発した「GPT」と呼ばれる言語モデルを利用しています。GPTはLLM（Large Language Models）と呼ばれる大規模言語モデルの一種です。OpenAI社は2022年11月にGPT-3.5を利用した「ChatGPT-3.5」を無料で公開し、2023年3月にはGPT-4.0を利用した「ChatGPT-4.0」を有料で公開しています。ChatGPT-4.0は、3.5よりも高精度で文書作成だけでなく画像・音楽・動画の生成も可能です。GPT-3.5とGPT-4.0はどちらも学習済みのAIであるため、新規にAIを学習させる必要がありません。利用者はただ質問を投げかけ、回答を得るだけです。ただし、回答が間違っている場合には間違っていることを伝えると、さらに学習を進めてより適切な回答を得られます。"
        interest = "スターウォーズ"
        web_page_content = WebPageContent(
            url="https://www.chatgpt.com/",
            title="ChatGPTとは？",
            content=content,
        )

        # WHEN: 個人最適化を行う
        result = self.service.personalize_content(
            prompty_filepath=prompty_filepath,
            web_page_content=web_page_content,
            interest=interest,
        )

        # THEN: 正しく個人最適化されたコンテンツが返されること
        assert result.url == web_page_content.url
        assert result.title == web_page_content.title
        assert result.content == web_page_content.content
        assert result.interest == interest
        assert isinstance(result.generated_at, datetime)
        assert result.personalized_content is not None
