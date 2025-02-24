from datetime import datetime

import prompty
import prompty.azure_beta
from prompty import Prompty

from ...config import settings
from ..models import PersonalizedWebPageContent, WebPageContent


class PersonalizeDomainService:
    """ドキュメントの個人最適化を行うドメインサービス"""

    def _get_prompty(self, prompty_filepath: str) -> Prompty:
        """個人最適化をするための実行クライアント取得

        Args:
            prompty_filepath (str): スクリプトを定義したpromptyファイル

        Returns:
            Prompty: Prompty class to define the prompty
        """
        prompty_ = prompty.load(prompty_filepath)

        if prompty_.model.configuration["type"].startswith("azure"):
            # NOTE: AzureOpenAIをたたく場合
            if prompty_.model.configuration.get("azure_deployment") is None:
                prompty_.model.configuration["azure_deployment"] = (
                    settings.deployment_name
                )
            if prompty_.model.configuration.get("azure_endpoint") is None:
                prompty_.model.configuration["azure_endpoint"] = settings.aoai_endpoint
            if prompty_.model.configuration.get("api_version") is None:
                prompty_.model.configuration["api_version"] = settings.aoai_api_version
            if prompty_.model.configuration.get("api_key") is None:
                prompty_.model.configuration["api_key"] = settings.aoai_api_key

        return prompty_

    def personalize_content(
        self, prompty_filepath: str, web_page_content: WebPageContent, interest: str
    ) -> PersonalizedWebPageContent:
        """Webページのコンテンツを個人最適化する

        Args:
            prompty_filepath (str): promptyファイルのパス
            web_page_content (WebPageContent): Webページのコンテンツ情報
            interest (str): 個人最適化のための興味関心

        Returns:
            PersonalizedWebPageContent: 個人最適化されたWebページのコンテンツ情報
        """
        prompty_ = self._get_prompty(prompty_filepath)

        personalized_content = prompty.execute(
            prompt=prompty_,
            inputs={"content": web_page_content.content, "interest": interest},
        )
        return PersonalizedWebPageContent(
            **web_page_content.model_dump(),
            interest=interest,
            generated_at=datetime.now(),
            personalized_content=personalized_content,
        )
