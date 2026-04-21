# fabric_sample

Microsoft Fabric の主要機能（Lakehouse / semantic model / オントロジー / レポート / Data Agent）を、
**CLI と VS Code + GitHub Copilot を中心に検証**するためのサンプルプロジェクトです。

## このリポジトリに含まれるもの

- `tools/generate_fabric_assets.py`
  - 業界を指定して、以下を一括生成するサンプルスクリプト
    - Bronze/Silver/Gold 用サンプルデータ（CSV）
    - semantic model 用テーブル/メジャー定義（JSON）
    - オントロジー（エンティティ定義 JSON）
- `.github/prompts/fabric-industry-sample.prompt.md`
  - GitHub Copilot に業界指定で生成を依頼しやすくするプロンプト（スキル）
- `.vscode/extensions.json`
  - 推奨 VS Code 拡張
- `.vscode/mcp.json`
  - MCP サーバー利用例（filesystem / github）
- `docs/setup-guide.md`
  - 検証環境セットアップ手順（GUI で設定する箇所も明記）
- `docs/medallion-architecture.md`
  - 本サンプルでのメダリオンアーキテクチャ解説

## クイックスタート

```bash
python3 /home/runner/work/fabric_sample/fabric_sample/tools/generate_fabric_assets.py \
  --industry retail \
  --records 500 \
  --output /home/runner/work/fabric_sample/fabric_sample/output/retail
```

生成された `output/<industry>` 配下を Fabric Lakehouse に取り込み、
`docs/setup-guide.md` の手順で semantic model・レポート・Data Agent まで確認します。

## Microsoft Learn（日本語）

以下は本プロジェクトで参照する公式ドキュメントです（リンク先は調査時点で有効な URL のみ記載）。

- Microsoft Fabric とは  
  https://learn.microsoft.com/ja-jp/fabric/fundamentals/microsoft-fabric-overview
- Lakehouse の概要  
  https://learn.microsoft.com/ja-jp/fabric/data-engineering/lakehouse-overview
- メダリオンアーキテクチャ（OneLake）  
  https://learn.microsoft.com/ja-jp/fabric/onelake/onelake-medallion-lakehouse-architecture
- セマンティック モデルの概要（Power BI）  
  https://learn.microsoft.com/ja-jp/power-bi/connect-data/service-datasets-understand
- Data Agent（Copilot と AI 機能の入口）  
  https://learn.microsoft.com/ja-jp/fabric/get-started/copilot-fabric-overview

詳細は `docs/setup-guide.md` を参照してください。
