# personaledge

特定のページから情報を取得し、個人の興味に合わせた具体例でその情報を説明してくれるツール

## 使い方

poetry 使ってライブラリ情報を入れてください

```bash
poetry install
```

### LLMの接続先情報を書く

**現状、Azure OpenAIにしか対応しておりませぬ🙇‍♂️**

今回、promptyを利用していますので、promptyファイルに接続先情報を書くか、プロジェクトルートに「.env」ファイルを作成してください。

#### promptyファイルに接続先情報を書く

「promots/sample.prompty」に接続先情報を書いてください。

```yaml
---
name: 普段のキャッチアップが楽しくなるような、個人の興味に合わせた表現をする情報収集アシスタント
description: 普段のキャッチアップが楽しくなるような、個人の興味に合わせた表現をする情報収集アシスタント
authors:
  - rakuichi
model:
  api: chat
  configuration:
    type: azure_openai
    azure_endpoint: <Azure OpenAI のエンドポイント>
    api_version: <Azure OpenAI API バージョン>
    api_key: <Azure OpenAI API 接続キー>
    azure_deployment: <モデルのデプロイメント名>

```

#### .envファイルに接続先情報を書く

```text
DEPLOYMENT_NAME=
AOAI_ENDPOINT=
AOAI_API_KEY=
AOAI_API_VERSION=
```

### スクリプトを動かす

プロジェクトルートにて以下コマンドを実行することで、特定のページに対して要約することができる

```bash
poetry run python single_page_script.py <url> <prompty_file（実行場所をrootとする） <interest（興味のある内容）> <slackのwebhok url(通知するなら)>
```

例

```bash
poetry run python single_page_script.py https://rakuichi4817.github.io/posts/2024/excalidraw-intro/ prompts/sample.prompty スターウォーズ 
```