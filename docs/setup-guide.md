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
python3 tools/generate_fabric_assets.py \
  --industry retail \
  --records 1000 \
  --output output/retail
```

## 5. Fabric ワークスペース構築（主に手動設定）

> ここは GUI 設定が中心。自動化より利用者操作の方が学習効果が高いため手動推奨。

1. **新規 Workspace を作成**
   - 作業: Fabric ポータルで「新しいワークスペース」を作成し、検証用の名前（例: `fabric-sample-retail`）を付けます。
   - 意図: 今回の検証用リソースを他案件と分離し、誤操作や設定混在を防ぎます。
2. **Workspace 内に Lakehouse を作成**
   - 作業: 作成した Workspace で Lakehouse を新規作成します。
   - 意図: Bronze / Silver / Gold データを OneLake 上で管理する基盤を用意します。
3. **ローカル生成データを Lakehouse に取り込む**
   - 作業: `output/<industry>/bronze`、`output/<industry>/silver`、`output/<industry>/gold` の CSV を、対応する階層が分かるようにアップロードします。
   - 意図: 後続の semantic model と Data Agent が参照する分析データを Fabric 側に配置します。
4. **Bronze→Silver→Gold の流れを確認**
   - 作業: Notebook または Dataflow Gen2 でテーブル内容を確認し、粗データ（Bronze）から整形済みデータ（Silver）、業務指標向けデータ（Gold）へ段階的に整理されているかを見ます。
   - 意図: メダリオンアーキテクチャのデータ品質向上プロセスを実データで理解します。

## 6. semantic model 設定

1. **テーブルとリレーションを定義**
   - 作業: `output/<industry>/semantic_model/tables.json` を参照し、事実テーブルとディメンションテーブルの関係を semantic model に設定します。
   - 意図: 集計時の結合ルールを明確にし、レポートや質問応答で一貫した数値が出るようにします。
2. **主要メジャーを作成**
   - 作業: `output/<industry>/semantic_model/measures.json` を参照し、`Total Sales`、`Average Order Value`、`Profit Margin` などのメジャーを作成します。
   - 意図: 再利用可能な計算指標をモデル側に集約し、レポート間の計算ロジック差異をなくします。
3. **メジャーの妥当性を初期確認**
   - 作業: 簡易ビジュアルを作って代表メジャーを表示し、明らかに不自然な値（0 固定、極端な負値など）がないか確認します。
   - 意図: 後工程（Data Agent / レポート）での手戻りを防ぐため、モデル品質を早期に担保します。

## 7. オントロジー / Data Agent 設定

1. **業務エンティティを定義**
   - 作業: `output/<industry>/ontology/entities.json` を参照し、Data Agent が理解すべき業務用語（例: 売上、顧客、商品カテゴリ、地域）を登録します。
   - 意図: 自然言語の質問をデータモデル上の列・指標に正しく対応付けるためです。
2. **Data Agent とデータソースを接続**
   - 作業: Data Agent に Gold 層テーブルと semantic model の主要メジャーを接続します。
   - 意図: Agent が「どのデータを使って答えるか」を明示し、回答の再現性を確保します。
3. **自然言語クエリを実行して挙動確認**
   - 作業: 次のような質問を実行し、意図した指標・粒度で回答が返るかを確認します。
     - 「先月の売上上位カテゴリを教えて」
     - 「利益率が低い地域はどこ？」
   - 意図: オントロジー定義と semantic model の接続が実運用に耐えるかを検証します。

## 8. レポート作成

1. **semantic model から新規レポートを作成**
   - 作業: 6章で作成した semantic model をデータソースとして新規レポートを作成します。
   - 意図: Data Agent と同じモデルを参照することで、分析基盤を統一します。
2. **基本ビジュアルを配置**
   - 作業: KPI カード（売上・利益率）、時系列推移、カテゴリ別内訳を配置します。
   - 意図: 経営指標・トレンド・構成比を一画面で確認できる最小構成を作ります。
3. **Data Agent との整合性を確認**
   - 作業: Data Agent の回答値とレポート表示値を照合し、同一条件で同一結果になることを確認します。
   - 意図: 会話型分析とBIレポートの結果を一致させ、利用者の信頼性を高めます。

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
