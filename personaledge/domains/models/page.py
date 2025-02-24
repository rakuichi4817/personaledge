from datetime import datetime

from pydantic import AnyHttpUrl, BaseModel, Field


class WebPageContent(BaseModel):
    """Webページのコンテンツ情報"""

    url: AnyHttpUrl = Field(..., description="ページのURL")
    title: str = Field(..., description="ページのタイトル")
    content: str = Field(..., description="HTML形式のコンテンツ")


class PersonalizedWebPageContent(WebPageContent):
    """個人最適化されたWebページのコンテンツ情報"""

    interest: str = Field(..., description="個人最適化のための興味関心")
    generated_at: datetime = Field(..., description="生成日時")
    personalized_content: str | None = Field(
        None, description="LLMにより個人最適化された情報"
    )
