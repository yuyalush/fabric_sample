# Microsoft Fabric 機能検証セットアップガイド

## 1. 目的

このガイドは、以下を一通り検証するための手順をまとめたものです。

- Lakehouse
- semantic model
- オントロジー（Data Agent 向けエンティティ設計）
- レポート作成
- Data Agent

## 2. 前提

- Microsoft Fabric が利用可能なテナント
- VS Code
- Python 3.10+
- GitHub Copilot（VS Code）

## 3. VS Code 準備

1. このリポジトリを VS Code で開く
2. 拡張機能の推奨を適用（`.vscode/extensions.json`）
3. 必要に応じて `.vscode/mcp.json` をローカル環境に合わせて調整

## 4. Copilot を使った業界別サンプル生成

1. VS Code の Copilot Chat で `.github/prompts/fabric-industry-sample.prompt.md` を実行
2. 業界（例: retail / healthcare / manufacturing / finance）を指定
3. 提案コマンドを実行してアセット生成

直接 CLI 実行する場合:

```bash
python3 /home/runner/work/fabric_sample/fabric_sample/tools/generate_fabric_assets.py \
  --industry retail \
  --records 1000 \
  --output /home/runner/work/fabric_sample/fabric_sample/output/retail
```

## 5. Fabric ワークスペース構築（主に手動設定）

> ここは GUI 設定が中心。自動化より利用者操作の方が学習効果が高いため手動推奨。

1. Fabric で新規 Workspace を作成
2. Lakehouse を作成
3. `output/<industry>/bronze|silver|gold` の CSV をアップロード
4. Notebook または Dataflow Gen2 で Bronze→Silver→Gold を確認

## 6. semantic model 設定

1. `output/<industry>/semantic_model/tables.json` を参照してテーブル関連を設定
2. `output/<industry>/semantic_model/measures.json` を参照してメジャー作成
3. 代表メジャー（Total Sales, Average Order Value, Profit Margin）を可視化

## 7. オントロジー / Data Agent 設定

1. `output/<industry>/ontology/entities.json` を参照して業務エンティティを作成
2. Data Agent にゴールド層テーブルと主要メジャーを接続
3. 自然言語クエリ例を実行
   - 「先月の売上上位カテゴリを教えて」
   - 「利益率が低い地域はどこ？」

## 8. レポート作成

1. semantic model から新規レポートを作成
2. KPI カード、時系列推移、カテゴリ別内訳を配置
3. Data Agent の回答とレポート数値の整合性を確認

## 9. 参考: Microsoft Learn（日本語）

- Fabric 概要  
  https://learn.microsoft.com/ja-jp/fabric/fundamentals/microsoft-fabric-overview
- Lakehouse 概要  
  https://learn.microsoft.com/ja-jp/fabric/data-engineering/lakehouse-overview
- OneLake メダリオンアーキテクチャ  
  https://learn.microsoft.com/ja-jp/fabric/onelake/onelake-medallion-lakehouse-architecture
- セマンティック モデル  
  https://learn.microsoft.com/ja-jp/power-bi/connect-data/service-datasets-understand
- Copilot / Data Agent 関連  
  https://learn.microsoft.com/ja-jp/fabric/get-started/copilot-fabric-overview
