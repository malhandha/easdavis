from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import requests

# ====================================
# APP
# ====================================

app = Flask(__name__)
CORS(app)

# ====================================
# LOAD DATA
# ====================================

df = pd.read_csv("sales.csv")

# ====================================
# CLEAN DATA
# ====================================

df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")
df["Profit"] = pd.to_numeric(df["Profit"], errors="coerce")

# ====================================
# KPI ENDPOINT
# ====================================

@app.route("/kpi")
def kpi():

    filtered_df = df.copy()

    # =========================
    # GET FILTER
    # =========================

    category = request.args.get("category")
    territory = request.args.get("territory")
    segment = request.args.get("segment")

    # =========================
    # APPLY FILTER
    # =========================

    if category and category != "All Category":
        filtered_df = filtered_df[
            filtered_df["Category"] == category
        ]

    if territory and territory != "All Territory":
        filtered_df = filtered_df[
            filtered_df["Territory"] == territory
        ]

    if segment and segment != "All Segment":
        filtered_df = filtered_df[
            filtered_df["Segment"] == segment
        ]

    # =========================
    # KPI
    # =========================

    total_sales = round(
        filtered_df["Sales"].sum(),
        2
    )

    total_profit = round(
        filtered_df["Profit"].sum(),
        2
    )

    total_orders = filtered_df[
        "SalesOrderID"
    ].nunique()

    profit_margin = 0

    if total_sales != 0:
        profit_margin = round(
            (total_profit / total_sales) * 100,
            2
        )

    return jsonify({
        "sales": total_sales,
        "profit": total_profit,
        "orders": int(total_orders),
        "margin": profit_margin
    })

# ====================================
# FILTER ENDPOINT
# ====================================

@app.route("/filters")
def filters():

    categories = []
    territories = []
    segments = []

    # CATEGORY
    if "Category" in df.columns:
        categories = sorted(
            df["Category"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

    # TERRITORY
    if "Territory" in df.columns:
        territories = sorted(
            df["Territory"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

    # SEGMENT
    if "Segment" in df.columns:
        segments = sorted(
            df["Segment"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

    return jsonify({
        "categories": categories,
        "territories": territories,
        "segments": segments
    })

# ====================================
# AI ANALYTICS
# ====================================

OLLAMA_URL = "http://localhost:11434/api/generate"

@app.route("/ask-ai", methods=["POST"])
def ask_ai():

    data = request.json

    prompt = data.get("prompt")

    # =========================
    # BUSINESS SUMMARY
    # =========================

    total_sales = round(df["Sales"].sum(), 2)

    total_profit = round(df["Profit"].sum(), 2)

    total_orders = df["SalesOrderID"].nunique()

    profit_margin = round(
        (total_profit / total_sales) * 100,
        2
    )

    # =========================
    # TOP PRODUCTS
    # =========================

    top_products = (
        df.groupby("ProductName")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )

    # =========================
    # TERRITORY SALES
    # =========================

    territory_sales = (
        df.groupby("Territory")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )

    # =========================
    # LOW PROFIT PRODUCTS
    # =========================

    low_profit = (
        df.groupby("ProductName")["Profit"]
        .sum()
        .sort_values()
        .head(5)
    )

    # =========================
    # AI PROMPT
    # =========================

    full_prompt = f"""
Kamu adalah AI Business Analyst profesional.

Gunakan bahasa Indonesia profesional.

DATA BISNIS:

Total Sales: {total_sales}
Total Profit: {total_profit}
Total Orders: {total_orders}
Profit Margin: {profit_margin}%

TOP PRODUCT:
{top_products}

TOP TERRITORY:
{territory_sales}

LOW PROFIT PRODUCT:
{low_profit}

TUGAS:
1. Analisis kondisi bisnis
2. Jelaskan insight penting
3. Deteksi anomali sederhana
4. Berikan rekomendasi strategis
5. Jawab dengan singkat namun profesional

PERTANYAAN USER:
{prompt}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "llama3",
            "prompt": full_prompt,
            "stream": False
        }
    )

    result = response.json()

    return jsonify({
        "response": result["response"]
    })

# ====================================
# HOME
# ====================================

@app.route("/")
def home():
    return "AI Dashboard Backend Running"

# ====================================
# RUN
# ====================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)