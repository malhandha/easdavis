from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

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

    category = request.args.get("category")
    territory = request.args.get("territory")
    segment = request.args.get("segment")

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
# FILTERS
# ====================================

@app.route("/filters")
def filters():

    categories = sorted(
        df["Category"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    territories = sorted(
        df["Territory"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

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
# AI
# ====================================

@app.route("/ask-ai", methods=["POST"])
def ask_ai():

    data = request.get_json()

    prompt = data.get("prompt", "")

    total_sales = round(df["Sales"].sum(), 2)
    total_profit = round(df["Profit"].sum(), 2)
    total_orders = df["SalesOrderID"].nunique()

    profit_margin = round(
        (total_profit / total_sales) * 100,
        2
    )

    top_products = (
        df.groupby("ProductName")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .to_string()
    )

    territory_sales = (
        df.groupby("Territory")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .to_string()
    )

    low_profit = (
        df.groupby("ProductName")["Profit"]
        .sum()
        .sort_values()
        .head(5)
        .to_string()
    )

    full_prompt = f"""
Kamu adalah AI Business Analyst profesional.

Gunakan bahasa Indonesia profesional.

DATA BISNIS

Total Sales: {total_sales}
Total Profit: {total_profit}
Total Orders: {total_orders}
Profit Margin: {profit_margin}%

TOP PRODUCT
{top_products}

TOP TERRITORY
{territory_sales}

LOW PROFIT PRODUCT
{low_profit}

TUGAS:
1. Analisis kondisi bisnis
2. Berikan insight penting
3. Berikan rekomendasi strategis
4. Jawab singkat dan profesional

PERTANYAAN USER:
{prompt}
"""

    chat_completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": full_prompt
            }
        ]
    )

    answer = chat_completion.choices[0].message.content

    return jsonify({
        "response": answer
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
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )