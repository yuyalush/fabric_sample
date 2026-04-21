# メダリオンアーキテクチャ解説（本サンプル）

本サンプルは Lakehouse 内で Bronze / Silver / Gold の3層を使います。

## Bronze

- 生データ層
- ファイル: `bronze/transactions_raw.csv`
- 特徴: 欠損やゆらぎを許容し、元データを保持

## Silver

- クレンジング・標準化層
- ファイル: `silver/transactions_clean.csv`
- 特徴: 型揃え、不要列除去、分析しやすいスキーマへ整形

## Gold

- ビジネス利用層
- ファイル: `gold/kpi_daily.csv`
- 特徴: KPI 集計済みでレポートや Data Agent から直接参照可能

## semantic model との関係

- Gold 層を中心にモデル化し、必要に応じて Silver を明細ドリルダウンに利用
- メジャーは `semantic_model/measures.json` を初期テンプレートとして使用

## オントロジーとの関係

- `ontology/entities.json` に、業務用語（顧客、商品、注文、地域など）を定義
- Data Agent が自然言語質問を解釈しやすいよう、エンティティの説明を付与
