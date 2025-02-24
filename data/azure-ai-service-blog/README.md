# 実行スクリプト

プロジェクトルートにて

```bash
python scripts/from_sitemap_to_dir.py https://techcommunity.microsoft.com/sitemap_azure-ai-services-blog.xml.gz prompts/sample.prompty スターウォーズ data/azure-ai-service-blog skip 10
```

実行条件

- 対象サイトマップ: <https://techcommunity.microsoft.com/sitemap_azure-ai-services-blog.xml.gz>
- プロンプトファイル: prompts/sample.prompty
- データ保存先: data/azure-ai-service-blog
- URLポストフィクス: なし（skipを入力）
- 実行時から何日以内の更新か: 10日以内