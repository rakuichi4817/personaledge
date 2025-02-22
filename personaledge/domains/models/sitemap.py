from datetime import datetime
from typing import Literal

from pydantic import AnyHttpUrl, BaseModel, Field


class SitemapUrl(BaseModel):
    """サイトマップの個別URL情報"""

    loc: AnyHttpUrl
    last_modified: datetime | None = Field(None, alias="lastmod")
    change_frequency: (
        Literal["always", "hourly", "daily", "weekly", "monthly", "yearly", "never"]
        | None
    ) = Field(None, alias="changefreq")
    priority: float | None = Field(None, ge=0, le=1)
