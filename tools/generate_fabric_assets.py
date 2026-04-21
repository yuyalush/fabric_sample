#!/usr/bin/env python3
import argparse
import csv
import json
import random
from datetime import date, timedelta
from pathlib import Path

INDUSTRY_PROFILES = {
    "retail": {
        "categories": ["アパレル", "家電", "ホーム", "ビューティー"],
        "subcategories": {
            "アパレル": ["メンズ", "レディース", "キッズ", "スポーツウェア"],
            "家電": ["スマートフォン", "パソコン", "オーディオ", "アクセサリ"],
            "ホーム": ["家具", "キッチン用品", "寝具", "インテリア"],
            "ビューティー": ["スキンケア", "メイクアップ", "ヘアケア", "フレグランス"],
        },
        "brands": ["スタイルα", "テックノバ", "ホームブリス", "グロウアップ", "エコウェア", "クイックバイ"],
        "regions": ["東日本", "西日本", "北日本", "南日本"],
        "prefecture_region_map": {
            "東日本": ["東京都", "神奈川県", "千葉県", "埼玉県"],
            "西日本": ["大阪府", "兵庫県", "京都府", "奈良県"],
            "北日本": ["北海道", "青森県", "宮城県", "福島県"],
            "南日本": ["福岡県", "鹿児島県", "沖縄県", "長崎県"],
        },
        "customer_segments": ["新規", "常連", "VIP", "休眠リスク", "離脱"],
        "payment_methods": ["クレジットカード", "デビットカード", "現金", "電子マネー", "後払い"],
        "stores": [f"店舗{i:03d}" for i in range(1, 21)],
    },
    "healthcare": {
        "categories": ["外来診療", "検査", "投薬", "手術"],
        "subcategories": {
            "外来診療": ["一般内科", "専門外来", "小児科", "老年内科"],
            "検査": ["血液検査", "画像診断", "病理検査", "遺伝子検査"],
            "投薬": ["市販薬", "処方薬", "サプリメント", "ワクチン"],
            "手術": ["待機手術", "緊急手術", "日帰り手術", "入院手術"],
        },
        "brands": [],
        "regions": ["東京圏", "大阪圏", "名古屋圏", "福岡圏"],
        "prefecture_region_map": {
            "東京圏": ["東京都", "神奈川県"],
            "大阪圏": ["大阪府", "兵庫県"],
            "名古屋圏": ["愛知県", "三重県"],
            "福岡圏": ["福岡県", "佐賀県"],
        },
        "customer_segments": ["外来患者", "入院患者", "救急患者", "慢性疾患"],
        "payment_methods": ["保険適用", "自費", "公費"],
        "stores": [f"クリニック{i:02d}" for i in range(1, 11)],
    },
    "manufacturing": {
        "categories": ["原材料", "組立", "検査", "出荷"],
        "subcategories": {
            "原材料": ["鉄鋼", "樹脂", "化学品", "繊維"],
            "組立": ["手動組立", "自動組立", "半自動", "外注"],
            "検査": ["外観検査", "寸法検査", "機能検査", "破壊検査"],
            "出荷": ["国内配送", "輸出", "急送便", "一括輸送"],
        },
        "brands": [],
        "regions": ["工場A", "工場B", "工場C"],
        "prefecture_region_map": {
            "工場A": ["愛知県", "静岡県"],
            "工場B": ["大阪府", "兵庫県"],
            "工場C": ["神奈川県", "東京都"],
        },
        "customer_segments": ["1次取引先", "2次取引先", "3次取引先"],
        "payment_methods": ["銀行振込", "信用状"],
        "stores": [f"ライン{i}" for i in range(1, 6)],
    },
    "finance": {
        "categories": ["融資", "預金", "保険", "投資"],
        "subcategories": {
            "融資": ["住宅ローン", "マイカーローン", "フリーローン", "事業資金"],
            "預金": ["普通預金", "定期預金", "当座預金", "外貨預金"],
            "保険": ["生命保険", "損害保険", "医療保険", "年金保険"],
            "投資": ["株式", "債券", "REIT", "FX"],
        },
        "brands": [],
        "regions": ["関東", "関西", "中部", "九州"],
        "prefecture_region_map": {
            "関東": ["東京都", "神奈川県", "埼玉県", "千葉県"],
            "関西": ["大阪府", "兵庫県", "京都府"],
            "中部": ["愛知県", "静岡県", "新潟県"],
            "九州": ["福岡県", "鹿児島県", "沖縄県"],
        },
        "customer_segments": ["個人", "中小企業", "法人", "プライベートバンキング"],
        "payment_methods": ["口座振替", "電信送金", "オンラインバンキング"],
        "stores": [f"支店{i:02d}" for i in range(1, 11)],
    },
}


def build_customers(industry: str, count: int = 200):
    """顧客マスタを生成する（Bronze 層: customers_raw / Silver 層: dim_customer）。"""
    profile = INDUSTRY_PROFILES.get(industry, INDUSTRY_PROFILES["retail"])
    age_groups = {
        range(18, 25): "18-24",
        range(25, 35): "25-34",
        range(35, 45): "35-44",
        range(45, 55): "45-54",
        range(55, 65): "55-64",
        range(65, 80): "65+",
    }
    rows = []
    for i in range(1, count + 1):
        region = random.choice(profile["regions"])
        prefecture_list = profile["prefecture_region_map"].get(region, [region])
        prefecture = random.choice(prefecture_list)
        age = random.randint(18, 79)
        age_group = next((v for k, v in age_groups.items() if age in k), "65+")
        reg_date = date.today() - timedelta(days=random.randint(30, 1800))
        segment = random.choice(profile["customer_segments"])
        rows.append(
            {
                "customer_id": f"C{i:05d}",
                "age": age,
                "gender": random.choice(["男性", "女性", "その他"]),
                "prefecture": prefecture,
                "region": region,
                "registration_date": reg_date.isoformat(),
                "customer_segment": segment,
                # Silver 派生列
                "age_group": age_group,
                "registration_year": reg_date.year,
            }
        )
    return rows


def build_products(industry: str):
    """商品マスタを生成する（Bronze 層: products_raw / Silver 層: dim_product）。"""
    profile = INDUSTRY_PROFILES.get(industry, INDUSTRY_PROFILES["retail"])
    brands = profile.get("brands") or ["Generic"]
    rows = []
    pid = 1
    for category, subs in profile["subcategories"].items():
        for sub in subs:
            standard_price = random.randint(500, 30000)
            standard_cost = int(standard_price * random.uniform(0.4, 0.75))
            rows.append(
                {
                    "product_id": f"P{pid:04d}",
                    "product_name": f"{sub}商品{pid:04d}",
                    "category": category,
                    "subcategory": sub,
                    "brand": random.choice(brands),
                    "standard_price": standard_price,
                    "standard_cost": standard_cost,
                }
            )
            pid += 1
    return rows


def build_dim_date(start: date, end: date):
    """日付ディメンションを生成する（Silver 層: dim_date）。"""
    rows = []
    current = start
    fiscal_month_offset = 3  # 4月始まり会計年度
    while current <= end:
        fiscal_month = ((current.month - 1 + fiscal_month_offset) % 12) + 1
        rows.append(
            {
                "date": current.isoformat(),
                "year": current.year,
                "month": current.month,
                "week": int(current.strftime("%V")),
                "quarter": (current.month - 1) // 3 + 1,
                "day_of_week": ["月曜日", "火曜日", "水曜日", "木曜日", "金曜日", "土曜日", "日曜日"][current.weekday()],
                "is_weekend": 1 if current.weekday() >= 5 else 0,
                "fiscal_month": fiscal_month,
            }
        )
        current += timedelta(days=1)
    return rows


def build_transactions(industry: str, records: int, customers, products):
    """トランザクション（ファクト）データを生成する。"""
    profile = INDUSTRY_PROFILES.get(industry, INDUSTRY_PROFILES["retail"])
    start = date.today() - timedelta(days=60)
    customer_ids = [c["customer_id"] for c in customers]
    product_map = {p["product_id"]: p for p in products}
    product_ids = list(product_map.keys())
    stores = profile["stores"]
    payment_methods = profile["payment_methods"]
    rows = []
    for i in range(1, records + 1):
        d = start + timedelta(days=random.randint(0, 59))
        pid = random.choice(product_ids)
        product = product_map[pid]
        qty = random.randint(1, 10)
        discount_rate = round(random.choice([0.0, 0.0, 0.0, 0.05, 0.10, 0.15, 0.20]), 2)
        unit_price = int(product["standard_price"] * (1 - discount_rate))
        unit_cost = product["standard_cost"]
        cid = random.choice(customer_ids)
        customer = next(c for c in customers if c["customer_id"] == cid)
        rows.append(
            {
                "transaction_id": i,
                "date": d.isoformat(),
                "industry": industry,
                "customer_id": cid,
                "product_id": pid,
                "store_id": random.choice(stores),
                "payment_method": random.choice(payment_methods),
                "category": product["category"],
                "subcategory": product["subcategory"],
                "region": customer["region"],
                "quantity": qty,
                "unit_price": unit_price,
                "unit_cost": unit_cost,
                "discount_rate": discount_rate,
            }
        )
    return rows


def write_csv(path: Path, rows, headers):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def aggregate_daily(rows):
    daily = {}
    for r in rows:
        key = r["date"]
        sales = r["quantity"] * r["unit_price"]
        cost = r["quantity"] * r["unit_cost"]
        rec = daily.setdefault(key, {"date": key, "sales": 0, "cost": 0, "orders": 0, "units": 0})
        rec["sales"] += sales
        rec["cost"] += cost
        rec["orders"] += 1
        rec["units"] += r["quantity"]
    out = []
    for key in sorted(daily.keys()):
        rec = daily[key]
        profit = rec["sales"] - rec["cost"]
        out.append(
            {
                "date": rec["date"],
                "sales": rec["sales"],
                "cost": rec["cost"],
                "profit": profit,
                "orders": rec["orders"],
                "units": rec["units"],
                "profit_margin": round((profit / rec["sales"]) if rec["sales"] else 0, 4),
            }
        )
    return out


def aggregate_weekly(rows):
    """週次集計（ISO 週番号 + 年で集計）。"""
    from datetime import datetime
    weekly = {}
    for r in rows:
        d = datetime.fromisoformat(r["date"])
        iso = d.isocalendar()
        key = (iso[0], iso[1])  # (year, week)
        sales = r["quantity"] * r["unit_price"]
        cost = r["quantity"] * r["unit_cost"]
        rec = weekly.setdefault(key, {"year": iso[0], "week": iso[1], "sales": 0, "cost": 0, "orders": 0, "units": 0})
        rec["sales"] += sales
        rec["cost"] += cost
        rec["orders"] += 1
        rec["units"] += r["quantity"]
    out = []
    for key in sorted(weekly.keys()):
        rec = weekly[key]
        profit = rec["sales"] - rec["cost"]
        out.append(
            {
                "year": rec["year"],
                "week": rec["week"],
                "sales": rec["sales"],
                "cost": rec["cost"],
                "profit": profit,
                "orders": rec["orders"],
                "units": rec["units"],
                "profit_margin": round((profit / rec["sales"]) if rec["sales"] else 0, 4),
            }
        )
    return out


def aggregate_monthly(rows):
    """月次集計（year-month で集計）。"""
    monthly = {}
    for r in rows:
        key = r["date"][:7]  # YYYY-MM
        sales = r["quantity"] * r["unit_price"]
        cost = r["quantity"] * r["unit_cost"]
        rec = monthly.setdefault(key, {"year_month": key, "sales": 0, "cost": 0, "orders": 0, "units": 0})
        rec["sales"] += sales
        rec["cost"] += cost
        rec["orders"] += 1
        rec["units"] += r["quantity"]
    out = []
    for key in sorted(monthly.keys()):
        rec = monthly[key]
        profit = rec["sales"] - rec["cost"]
        out.append(
            {
                "year_month": rec["year_month"],
                "sales": rec["sales"],
                "cost": rec["cost"],
                "profit": profit,
                "orders": rec["orders"],
                "units": rec["units"],
                "profit_margin": round((profit / rec["sales"]) if rec["sales"] else 0, 4),
            }
        )
    return out


def aggregate_by_category(rows):
    """カテゴリ別累計集計。"""
    cat = {}
    for r in rows:
        key = (r["category"], r.get("subcategory", ""))
        sales = r["quantity"] * r["unit_price"]
        cost = r["quantity"] * r["unit_cost"]
        rec = cat.setdefault(key, {"category": key[0], "subcategory": key[1], "sales": 0, "cost": 0, "orders": 0, "units": 0})
        rec["sales"] += sales
        rec["cost"] += cost
        rec["orders"] += 1
        rec["units"] += r["quantity"]
    out = []
    for key in sorted(cat.keys()):
        rec = cat[key]
        profit = rec["sales"] - rec["cost"]
        out.append(
            {
                "category": rec["category"],
                "subcategory": rec["subcategory"],
                "sales": rec["sales"],
                "cost": rec["cost"],
                "profit": profit,
                "orders": rec["orders"],
                "units": rec["units"],
                "profit_margin": round((profit / rec["sales"]) if rec["sales"] else 0, 4),
            }
        )
    return out


def aggregate_by_region(rows):
    """地域別累計集計。"""
    reg = {}
    for r in rows:
        key = r["region"]
        sales = r["quantity"] * r["unit_price"]
        cost = r["quantity"] * r["unit_cost"]
        rec = reg.setdefault(key, {"region": key, "sales": 0, "cost": 0, "orders": 0, "units": 0})
        rec["sales"] += sales
        rec["cost"] += cost
        rec["orders"] += 1
        rec["units"] += r["quantity"]
    out = []
    for key in sorted(reg.keys()):
        rec = reg[key]
        profit = rec["sales"] - rec["cost"]
        out.append(
            {
                "region": rec["region"],
                "sales": rec["sales"],
                "cost": rec["cost"],
                "profit": profit,
                "orders": rec["orders"],
                "units": rec["units"],
                "profit_margin": round((profit / rec["sales"]) if rec["sales"] else 0, 4),
            }
        )
    return out


def build_top_products(rows, products, top_n: int = 20):
    """商品別売上ランキング（Gold 層: top_products）。"""
    product_map = {p["product_id"]: p for p in products}
    prod = {}
    for r in rows:
        pid = r["product_id"]
        sales = r["quantity"] * r["unit_price"]
        cost = r["quantity"] * r["unit_cost"]
        rec = prod.setdefault(pid, {"product_id": pid, "sales": 0, "cost": 0, "orders": 0, "units": 0})
        rec["sales"] += sales
        rec["cost"] += cost
        rec["orders"] += 1
        rec["units"] += r["quantity"]
    ranked = sorted(prod.values(), key=lambda x: x["sales"], reverse=True)[:top_n]
    out = []
    for rank, rec in enumerate(ranked, start=1):
        p = product_map.get(rec["product_id"], {})
        profit = rec["sales"] - rec["cost"]
        out.append(
            {
                "rank": rank,
                "product_id": rec["product_id"],
                "product_name": p.get("product_name", ""),
                "category": p.get("category", ""),
                "subcategory": p.get("subcategory", ""),
                "brand": p.get("brand", ""),
                "sales": rec["sales"],
                "cost": rec["cost"],
                "profit": profit,
                "orders": rec["orders"],
                "units": rec["units"],
                "profit_margin": round((profit / rec["sales"]) if rec["sales"] else 0, 4),
            }
        )
    return out


def write_json(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Generate Microsoft Fabric sample assets")
    parser.add_argument("--industry", default="retail", help="retail|healthcare|manufacturing|finance")
    parser.add_argument("--records", type=int, default=1000)
    parser.add_argument("--customers", type=int, default=200)
    parser.add_argument("--output", default="output/retail")
    args = parser.parse_args()

    industry = args.industry.lower()
    output_dir = Path(args.output)

    # ── マスタ生成 ─────────────────────────────────────────────────────────────
    customers = build_customers(industry, args.customers)
    products = build_products(industry)

    # ── ファクト生成 ───────────────────────────────────────────────────────────
    raw_rows = build_transactions(industry, args.records, customers, products)

    # ── Silver 派生 ────────────────────────────────────────────────────────────
    clean_rows = []
    for r in raw_rows:
        sales_amount = r["quantity"] * r["unit_price"]
        cost_amount = r["quantity"] * r["unit_cost"]
        profit = sales_amount - cost_amount
        clean_rows.append(
            {
                **r,
                "sales_amount": sales_amount,
                "cost_amount": cost_amount,
                "profit": profit,
                "profit_margin": round(profit / sales_amount if sales_amount else 0, 4),
                "is_discounted": 1 if r["discount_rate"] > 0 else 0,
            }
        )

    # 日付ディメンション範囲
    from datetime import date as _date, timedelta as _td
    dim_start = _date.today() - _td(days=60)
    dim_end = _date.today()
    dim_date_rows = build_dim_date(dim_start, dim_end)

    # ── Gold 集計 ──────────────────────────────────────────────────────────────
    kpi_daily = aggregate_daily(raw_rows)
    kpi_weekly = aggregate_weekly(raw_rows)
    kpi_monthly = aggregate_monthly(raw_rows)
    kpi_by_category = aggregate_by_category(raw_rows)
    kpi_by_region = aggregate_by_region(raw_rows)
    top_products = build_top_products(raw_rows, products)

    # ── Bronze 書き出し ────────────────────────────────────────────────────────
    write_csv(
        output_dir / "bronze" / "transactions_raw.csv",
        raw_rows,
        [
            "transaction_id", "date", "industry", "customer_id", "product_id",
            "store_id", "payment_method", "category", "subcategory", "region",
            "quantity", "unit_price", "unit_cost", "discount_rate",
        ],
    )
    write_csv(
        output_dir / "bronze" / "customers_raw.csv",
        customers,
        [
            "customer_id", "age", "gender", "prefecture", "region",
            "registration_date", "customer_segment", "age_group", "registration_year",
        ],
    )
    write_csv(
        output_dir / "bronze" / "products_raw.csv",
        products,
        ["product_id", "product_name", "category", "subcategory", "brand", "standard_price", "standard_cost"],
    )

    # ── Silver 書き出し ────────────────────────────────────────────────────────
    write_csv(
        output_dir / "silver" / "transactions_clean.csv",
        clean_rows,
        [
            "transaction_id", "date", "industry", "customer_id", "product_id",
            "store_id", "payment_method", "category", "subcategory", "region",
            "quantity", "unit_price", "unit_cost", "discount_rate",
            "sales_amount", "cost_amount", "profit", "profit_margin", "is_discounted",
        ],
    )
    dim_customer_rows = [
        {k: c[k] for k in ["customer_id", "age_group", "gender", "prefecture", "region", "customer_segment", "registration_year"]}
        for c in customers
    ]
    write_csv(
        output_dir / "silver" / "dim_customer.csv",
        dim_customer_rows,
        ["customer_id", "age_group", "gender", "prefecture", "region", "customer_segment", "registration_year"],
    )
    dim_product_rows = [
        {k: p[k] for k in ["product_id", "product_name", "category", "subcategory", "brand"]}
        for p in products
    ]
    write_csv(
        output_dir / "silver" / "dim_product.csv",
        dim_product_rows,
        ["product_id", "product_name", "category", "subcategory", "brand"],
    )
    write_csv(
        output_dir / "silver" / "dim_date.csv",
        dim_date_rows,
        ["date", "year", "month", "week", "quarter", "day_of_week", "is_weekend", "fiscal_month"],
    )

    # ── Gold 書き出し ──────────────────────────────────────────────────────────
    write_csv(
        output_dir / "gold" / "kpi_daily.csv",
        kpi_daily,
        ["date", "sales", "cost", "profit", "orders", "units", "profit_margin"],
    )
    write_csv(
        output_dir / "gold" / "kpi_weekly.csv",
        kpi_weekly,
        ["year", "week", "sales", "cost", "profit", "orders", "units", "profit_margin"],
    )
    write_csv(
        output_dir / "gold" / "kpi_monthly.csv",
        kpi_monthly,
        ["year_month", "sales", "cost", "profit", "orders", "units", "profit_margin"],
    )
    write_csv(
        output_dir / "gold" / "kpi_by_category.csv",
        kpi_by_category,
        ["category", "subcategory", "sales", "cost", "profit", "orders", "units", "profit_margin"],
    )
    write_csv(
        output_dir / "gold" / "kpi_by_region.csv",
        kpi_by_region,
        ["region", "sales", "cost", "profit", "orders", "units", "profit_margin"],
    )
    write_csv(
        output_dir / "gold" / "top_products.csv",
        top_products,
        ["rank", "product_id", "product_name", "category", "subcategory", "brand",
         "sales", "cost", "profit", "orders", "units", "profit_margin"],
    )

    # ── Semantic Model JSON ────────────────────────────────────────────────────
    write_json(
        output_dir / "semantic_model" / "tables.json",
        {
            "tables": [
                {
                    "name": "Fact_Transactions",
                    "source": "silver/transactions_clean.csv",
                    "grain": "transaction",
                    "description": "1行1取引のファクトテーブル",
                },
                {
                    "name": "Dim_Customer",
                    "source": "silver/dim_customer.csv",
                    "grain": "customer",
                    "description": "顧客ディメンションテーブル",
                },
                {
                    "name": "Dim_Product",
                    "source": "silver/dim_product.csv",
                    "grain": "product",
                    "description": "商品ディメンションテーブル",
                },
                {
                    "name": "Dim_Date",
                    "source": "silver/dim_date.csv",
                    "grain": "date",
                    "description": "日付ディメンションテーブル（週次・月次・会計月含む）",
                },
                {
                    "name": "KPI_Daily",
                    "source": "gold/kpi_daily.csv",
                    "grain": "date",
                    "description": "日次 KPI 集計（売上・利益率など）",
                },
                {
                    "name": "KPI_Monthly",
                    "source": "gold/kpi_monthly.csv",
                    "grain": "year_month",
                    "description": "月次 KPI 集計",
                },
            ],
            "relationships": [
                {
                    "from": "Fact_Transactions.customer_id",
                    "to": "Dim_Customer.customer_id",
                    "type": "many-to-one",
                    "active": True,
                },
                {
                    "from": "Fact_Transactions.product_id",
                    "to": "Dim_Product.product_id",
                    "type": "many-to-one",
                    "active": True,
                },
                {
                    "from": "Fact_Transactions.date",
                    "to": "Dim_Date.date",
                    "type": "many-to-one",
                    "active": True,
                },
                {
                    "from": "KPI_Daily.date",
                    "to": "Dim_Date.date",
                    "type": "many-to-one",
                    "active": True,
                },
            ],
        },
    )

    write_json(
        output_dir / "semantic_model" / "measures.json",
        {
            "measures": [
                {
                    "name": "Total Sales",
                    "expression": "SUM('Fact_Transactions'[sales_amount])",
                    "format": "#,##0",
                },
                {
                    "name": "Total Cost",
                    "expression": "SUM('Fact_Transactions'[cost_amount])",
                    "format": "#,##0",
                },
                {
                    "name": "Profit",
                    "expression": "[Total Sales] - [Total Cost]",
                    "format": "#,##0",
                },
                {
                    "name": "Profit Margin",
                    "expression": "DIVIDE([Profit], [Total Sales])",
                    "format": "0.00%",
                },
                {
                    "name": "Average Order Value",
                    "expression": "DIVIDE([Total Sales], DISTINCTCOUNT('Fact_Transactions'[transaction_id]))",
                    "format": "#,##0",
                },
                {
                    "name": "Unique Customers",
                    "expression": "DISTINCTCOUNT('Fact_Transactions'[customer_id])",
                    "format": "#,##0",
                },
                {
                    "name": "Units Sold",
                    "expression": "SUM('Fact_Transactions'[quantity])",
                    "format": "#,##0",
                },
                {
                    "name": "Average Discount Rate",
                    "expression": "AVERAGE('Fact_Transactions'[discount_rate])",
                    "format": "0.00%",
                },
                {
                    "name": "Last Month Sales",
                    "expression": "CALCULATE([Total Sales], DATEADD('Dim_Date'[date], -1, MONTH))",
                    "format": "#,##0",
                },
                {
                    "name": "MoM Sales Growth",
                    "expression": "DIVIDE([Total Sales] - [Last Month Sales], [Last Month Sales])",
                    "format": "0.00%",
                },
            ]
        },
    )

    # ── Ontology JSON ──────────────────────────────────────────────────────────
    write_json(
        output_dir / "ontology" / "entities.json",
        {
            "entities": [
                {
                    "name": "Customer",
                    "description": f"{industry}業界の顧客",
                    "attributes": [
                        {"name": "customer_id", "type": "string", "description": "顧客識別子"},
                        {"name": "age_group", "type": "string", "description": "年齢層（例: 25-34）"},
                        {"name": "gender", "type": "string", "description": "性別（M/F/Other）"},
                        {"name": "prefecture", "type": "string", "description": "都道府県"},
                        {"name": "region", "type": "string", "description": "地域区分"},
                        {"name": "customer_segment", "type": "string", "description": "顧客セグメント（例: New, VIP）"},
                        {"name": "registration_year", "type": "integer", "description": "登録年（新規/既存判定に利用）"},
                    ],
                    "maps_to": "Dim_Customer",
                },
                {
                    "name": "Product",
                    "description": f"{industry}業界の商品・サービス",
                    "attributes": [
                        {"name": "product_id", "type": "string", "description": "商品識別子"},
                        {"name": "product_name", "type": "string", "description": "商品名"},
                        {"name": "category", "type": "string", "description": "大カテゴリ"},
                        {"name": "subcategory", "type": "string", "description": "小カテゴリ"},
                        {"name": "brand", "type": "string", "description": "ブランド名"},
                    ],
                    "maps_to": "Dim_Product",
                },
                {
                    "name": "Transaction",
                    "description": "売上取引の1件",
                    "attributes": [
                        {"name": "transaction_id", "type": "integer", "description": "取引識別子"},
                        {"name": "date", "type": "date", "description": "取引日"},
                        {"name": "sales_amount", "type": "integer", "description": "売上金額"},
                        {"name": "cost_amount", "type": "integer", "description": "原価金額"},
                        {"name": "profit", "type": "integer", "description": "利益"},
                        {"name": "quantity", "type": "integer", "description": "販売数量"},
                        {"name": "discount_rate", "type": "float", "description": "割引率（0.0〜0.2）"},
                        {"name": "payment_method", "type": "string", "description": "支払い方法"},
                    ],
                    "maps_to": "Fact_Transactions",
                },
                {
                    "name": "Region",
                    "description": "地域区分と都道府県のマッピング",
                    "attributes": [
                        {"name": "region", "type": "string", "description": "地域区分（例: East, West）"},
                        {"name": "prefecture", "type": "string", "description": "都道府県名"},
                    ],
                    "maps_to": "Dim_Customer",
                },
                {
                    "name": "KPI",
                    "description": "売上・利益率・成長率などの重要業績指標",
                    "attributes": [
                        {"name": "Total Sales", "type": "measure", "description": "期間内合計売上"},
                        {"name": "Profit Margin", "type": "measure", "description": "利益率（利益÷売上）"},
                        {"name": "MoM Sales Growth", "type": "measure", "description": "前月比売上成長率"},
                        {"name": "Unique Customers", "type": "measure", "description": "ユニーク購入顧客数"},
                        {"name": "Average Order Value", "type": "measure", "description": "1注文あたり平均売上"},
                    ],
                    "maps_to": "semantic_model/measures",
                },
                {
                    "name": "DatePeriod",
                    "description": "分析対象期間（日・週・月・四半期・会計月）",
                    "attributes": [
                        {"name": "date", "type": "date", "description": "日付"},
                        {"name": "week", "type": "integer", "description": "ISO 週番号"},
                        {"name": "month", "type": "integer", "description": "月"},
                        {"name": "quarter", "type": "integer", "description": "四半期"},
                        {"name": "is_weekend", "type": "integer", "description": "週末フラグ（1=土日）"},
                        {"name": "fiscal_month", "type": "integer", "description": "会計月（4月始まり）"},
                    ],
                    "maps_to": "Dim_Date",
                },
            ]
        },
    )

    # ── Data Agent クエリシナリオ JSON ─────────────────────────────────────────
    write_json(
        output_dir / "query_scenarios.json",
        {
            "industry": industry,
            "scenarios": [
                {
                    "id": 1,
                    "question": "先月の売上上位カテゴリを教えて",
                    "expected_tables": ["Fact_Transactions", "Dim_Product", "Dim_Date"],
                    "expected_measures": ["Total Sales"],
                    "expected_dimensions": ["category"],
                    "filter": "先月分",
                },
                {
                    "id": 2,
                    "question": "地域別の利益率を比較して",
                    "expected_tables": ["Fact_Transactions", "Dim_Customer"],
                    "expected_measures": ["Profit Margin"],
                    "expected_dimensions": ["region"],
                    "filter": "全期間",
                },
                {
                    "id": 3,
                    "question": "女性顧客の購入傾向を分析して",
                    "expected_tables": ["Fact_Transactions", "Dim_Customer", "Dim_Product"],
                    "expected_measures": ["Total Sales", "Unique Customers", "Average Order Value"],
                    "expected_dimensions": ["gender", "category"],
                    "filter": "性別=女性",
                },
                {
                    "id": 4,
                    "question": "今月の売上は前月比でどう変化した？",
                    "expected_tables": ["Fact_Transactions", "Dim_Date"],
                    "expected_measures": ["Total Sales", "MoM Sales Growth"],
                    "expected_dimensions": ["year_month"],
                    "filter": "当月 vs 先月",
                },
                {
                    "id": 5,
                    "question": "最も売れている商品ブランドはどれ？",
                    "expected_tables": ["Fact_Transactions", "Dim_Product"],
                    "expected_measures": ["Total Sales", "Units Sold"],
                    "expected_dimensions": ["brand"],
                    "filter": "全期間",
                },
                {
                    "id": 6,
                    "question": "割引率が高い取引はどれくらいある？",
                    "expected_tables": ["Fact_Transactions"],
                    "expected_measures": ["Average Discount Rate"],
                    "expected_dimensions": ["is_discounted"],
                    "filter": "割引率 > 0",
                },
                {
                    "id": 7,
                    "question": "週末と平日の売上パターンの違いは？",
                    "expected_tables": ["Fact_Transactions", "Dim_Date"],
                    "expected_measures": ["Total Sales", "Average Order Value"],
                    "expected_dimensions": ["is_weekend"],
                    "filter": "週末フラグ 0または1",
                },
                {
                    "id": 8,
                    "question": "新規顧客と既存顧客の購買行動の違いを教えて",
                    "expected_tables": ["Fact_Transactions", "Dim_Customer"],
                    "expected_measures": ["Total Sales", "Average Order Value", "Unique Customers"],
                    "expected_dimensions": ["customer_segment", "registration_year"],
                    "filter": "顧客セグメント in [新規, 常連, VIP]",
                },
            ],
        },
    )

    print(f"Generated Fabric assets for '{industry}' at: {output_dir.resolve()}")
    print(f"  Bronze : transactions_raw.csv, customers_raw.csv, products_raw.csv")
    print(f"  Silver : transactions_clean.csv, dim_customer.csv, dim_product.csv, dim_date.csv")
    print(f"  Gold   : kpi_daily.csv, kpi_weekly.csv, kpi_monthly.csv,")
    print(f"           kpi_by_category.csv, kpi_by_region.csv, top_products.csv")
    print(f"  Model  : semantic_model/tables.json, semantic_model/measures.json")
    print(f"  Onto   : ontology/entities.json")
    print(f"  Agent  : query_scenarios.json")


if __name__ == "__main__":
    main()
