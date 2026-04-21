#!/usr/bin/env python3
import argparse
import csv
import json
import random
from datetime import date, timedelta
from pathlib import Path

INDUSTRY_PROFILES = {
    "retail": {
        "categories": ["Apparel", "Electronics", "Home", "Beauty"],
        "regions": ["East", "West", "North", "South"],
    },
    "healthcare": {
        "categories": ["Consultation", "Lab", "Medication", "Surgery"],
        "regions": ["Tokyo", "Osaka", "Nagoya", "Fukuoka"],
    },
    "manufacturing": {
        "categories": ["RawMaterial", "Assembly", "Inspection", "Shipment"],
        "regions": ["Plant-A", "Plant-B", "Plant-C"],
    },
    "finance": {
        "categories": ["Loan", "Deposit", "Insurance", "Investment"],
        "regions": ["Kanto", "Kansai", "Chubu", "Kyushu"],
    },
}


def build_transactions(industry: str, records: int):
    profile = INDUSTRY_PROFILES.get(industry, INDUSTRY_PROFILES["retail"])
    start = date.today() - timedelta(days=60)
    rows = []
    for i in range(1, records + 1):
        d = start + timedelta(days=random.randint(0, 59))
        qty = random.randint(1, 10)
        unit_price = random.randint(1000, 25000)
        cost = int(unit_price * random.uniform(0.55, 0.9))
        rows.append(
            {
                "transaction_id": i,
                "date": d.isoformat(),
                "industry": industry,
                "category": random.choice(profile["categories"]),
                "region": random.choice(profile["regions"]),
                "quantity": qty,
                "unit_price": unit_price,
                "unit_cost": cost,
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
        rec = daily.setdefault(key, {"date": key, "sales": 0, "cost": 0, "orders": 0})
        rec["sales"] += sales
        rec["cost"] += cost
        rec["orders"] += 1
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
    parser.add_argument("--output", default="output/retail")
    args = parser.parse_args()

    industry = args.industry.lower()
    output_dir = Path(args.output)

    raw_rows = build_transactions(industry, args.records)
    clean_rows = [
        {
            **r,
            "sales_amount": r["quantity"] * r["unit_price"],
            "cost_amount": r["quantity"] * r["unit_cost"],
        }
        for r in raw_rows
    ]
    kpi_rows = aggregate_daily(raw_rows)

    write_csv(
        output_dir / "bronze" / "transactions_raw.csv",
        raw_rows,
        ["transaction_id", "date", "industry", "category", "region", "quantity", "unit_price", "unit_cost"],
    )
    write_csv(
        output_dir / "silver" / "transactions_clean.csv",
        clean_rows,
        [
            "transaction_id",
            "date",
            "industry",
            "category",
            "region",
            "quantity",
            "unit_price",
            "unit_cost",
            "sales_amount",
            "cost_amount",
        ],
    )
    write_csv(
        output_dir / "gold" / "kpi_daily.csv",
        kpi_rows,
        ["date", "sales", "cost", "profit", "orders", "profit_margin"],
    )

    write_json(
        output_dir / "semantic_model" / "tables.json",
        {
            "tables": [
                {"name": "Transactions", "source": "silver/transactions_clean.csv", "grain": "transaction"},
                {"name": "KPI Daily", "source": "gold/kpi_daily.csv", "grain": "date"},
            ],
            "relationships": [{"from": "Transactions.date", "to": "KPI Daily.date", "type": "many-to-one"}],
        },
    )

    write_json(
        output_dir / "semantic_model" / "measures.json",
        {
            "measures": [
                {"name": "Total Sales", "expression": "SUM('Transactions'[sales_amount])"},
                {"name": "Total Cost", "expression": "SUM('Transactions'[cost_amount])"},
                {
                    "name": "Profit",
                    "expression": "[Total Sales] - [Total Cost]",
                },
                {
                    "name": "Average Order Value",
                    "expression": "DIVIDE([Total Sales], DISTINCTCOUNT('Transactions'[transaction_id]))",
                },
                {
                    "name": "Profit Margin",
                    "expression": "DIVIDE([Profit], [Total Sales])",
                },
            ]
        },
    )

    write_json(
        output_dir / "ontology" / "entities.json",
        {
            "entities": [
                {"name": "CustomerSegment", "description": f"{industry}業界の顧客セグメント"},
                {"name": "ProductOrService", "description": f"{industry}業界のカテゴリ"},
                {"name": "Region", "description": "地域区分"},
                {"name": "Order", "description": "取引単位"},
                {"name": "KPI", "description": "売上・利益率などの重要指標"},
            ]
        },
    )

    print(f"Generated Fabric assets for '{industry}' at: {output_dir.resolve()}")


if __name__ == "__main__":
    main()
