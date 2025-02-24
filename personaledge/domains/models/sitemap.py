from datetime import datetime
from typing import Literal

from pydantic import AnyHttpUrl, BaseModel, Field, field_validator

from ...config import tz


class SitemapPage(BaseModel):
    """サイトマップの個別URL情報"""

    loc: AnyHttpUrl
    last_modified: datetime | None = Field(
        None,
    )
    change_frequency: (
        Literal["always", "hourly", "daily", "weekly", "monthly", "yearly", "never"]
        | None
    ) = Field(None)
    priority: float | None = Field(None, ge=0, le=1)

    @field_validator("last_modified")
    def validate_last_modified(cls, value, values):
        # ローカルタイムゾーンに変換
        if value is not None:
            return datetime.fromtimestamp(value.timestamp(), tz=tz)
