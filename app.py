
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Market Basket Analysis",
    page_icon="🛒",
    layout="wide"
)


# ==========================================
# CUSTOM STYLING
# ==========================================

st.markdown(
    """
    <style>
    .main {
        padding-top: 1rem;
    }

    h1 {
        color: #1f4e79;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================
# LOAD AND PROCESS DATA
# ==========================================

@st.cache_data
def load_data():

    df = pd.read_excel("Online Retail.xlsx")

    # Remove missing values
    df = df.dropna(
        subset=["InvoiceNo", "Description"]
    )

    # Remove cancelled invoices
    df = df[
        ~df["InvoiceNo"]
        .astype(str)
        .str.startswith("C")
    ]

    # Remove invalid quantities
    df = df[df["Quantity"] > 0]

    # Keep only the top 150 products
    # to reduce memory usage
    top_products = (
        df["Description"]
        .value_counts()
        .head(150)
        .index
    )

    df = df[
        df["Description"].isin(top_products)
    ]

    # Create transaction basket
    basket = df.pivot_table(
        index="InvoiceNo",
        columns="Description",
        values="Quantity",
        aggfunc="sum",
        fill_value=0
    )

    # Convert quantity into binary values
    basket = basket.apply(
        lambda column: column.map(
            lambda value: 1 if value > 0 else 0
        )
    )

    return df, basket


# ==========================================
# DASHBOARD HEADER
# ==========================================

st.title("🛒 Market Basket Analysis Dashboard")

st.markdown(
    """
    This dashboard discovers customer purchasing
    patterns using the **Apriori algorithm**.

    **Business Objective:** Identify products that
    customers frequently purchase together.
    """
)


# ==========================================
# LOAD DATASET
# ==========================================

try:

    df, basket = load_data()

except Exception as error:

    st.error(
        "Dataset could not be loaded. "
        "Ensure Online Retail.xlsx is in the same "
        "folder as app.py."
    )

    st.stop()


# ==========================================
# SIDEBAR SETTINGS
# ==========================================

st.sidebar.header("⚙️ Dashboard Settings")

min_support = st.sidebar.slider(
    "Minimum Support",
    min_value=0.01,
    max_value=0.10,
    value=0.02,
    step=0.01
)

min_confidence = st.sidebar.slider(
    "Minimum Confidence",
    min_value=0.10,
    max_value=1.00,
    value=0.30,
    step=0.05
)


# ==========================================
# APRIORI ALGORITHM
# ==========================================

frequent_itemsets = apriori(
    basket,
    min_support=min_support,
    use_colnames=True,
    max_len=2,
    low_memory=True
)


# ==========================================
# ASSOCIATION RULES
# ==========================================

if len(frequent_itemsets) > 1:

    rules = association_rules(
        frequent_itemsets,
        metric="confidence",
        min_threshold=min_confidence
    )

    useful_rules = rules[
        rules["lift"] > 1
    ].sort_values(
        by="lift",
        ascending=False
    )

else:

    useful_rules = pd.DataFrame()


# ==========================================
# KPI CARDS
# ==========================================

st.subheader("📊 Dataset Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Total Transactions",
        f"{basket.shape[0]:,}"
    )

with col2:

    st.metric(
        "Products Analyzed",
        f"{basket.shape[1]:,}"
    )

with col3:

    st.metric(
        "Frequent Itemsets",
        f"{len(frequent_itemsets):,}"
    )

with col4:

    st.metric(
        "Useful Rules",
        f"{len(useful_rules):,}"
    )


# ==========================================
# TOP PRODUCTS ANALYSIS
# ==========================================

st.subheader("🏷️ Top 10 Products by Quantity")

top_products_chart = (
    df.groupby("Description")["Quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig1, ax1 = plt.subplots(figsize=(10, 5))

top_products_chart.sort_values().plot(
    kind="barh",
    ax=ax1
)

ax1.set_title(
    "Top 10 Products by Quantity Sold"
)

ax1.set_xlabel("Quantity Sold")
ax1.set_ylabel("Product")

plt.tight_layout()

st.pyplot(fig1)

plt.close(fig1)


# ==========================================
# FREQUENT ITEMSETS
# ==========================================

st.subheader("🔗 Top Frequent Itemsets")

if len(frequent_itemsets) > 0:

    top_itemsets = (
        frequent_itemsets
        .sort_values(
            by="support",
            ascending=False
        )
        .head(10)
        .copy()
    )

    top_itemsets["itemsets"] = (
        top_itemsets["itemsets"]
        .apply(
            lambda items: ", ".join(
                sorted(items)
            )
        )
    )

    st.dataframe(
        top_itemsets,
        use_container_width=True
    )

else:

    st.warning(
        "No frequent itemsets found. "
        "Try reducing Minimum Support."
    )


# ==========================================
# ASSOCIATION RULES TABLE
# ==========================================

st.subheader("📋 Top Association Rules")

if len(useful_rules) > 0:

    top_rules = (
        useful_rules
        .head(10)
        .copy()
    )

    top_rules["antecedents"] = (
        top_rules["antecedents"]
        .apply(
            lambda items: ", ".join(
                sorted(items)
            )
        )
    )

    top_rules["consequents"] = (
        top_rules["consequents"]
        .apply(
            lambda items: ", ".join(
                sorted(items)
            )
        )
    )

    st.dataframe(
        top_rules[
            [
                "antecedents",
                "consequents",
                "support",
                "confidence",
                "lift"
            ]
        ],
        use_container_width=True
    )

else:

    st.warning(
        "No useful association rules found. "
        "Try reducing Minimum Confidence."
    )


# ==========================================
# CONFIDENCE VS LIFT CHART
# ==========================================

st.subheader("📈 Confidence vs Lift")

if len(useful_rules) > 0:

    fig2, ax2 = plt.subplots(figsize=(10, 5))

    ax2.scatter(
        useful_rules["confidence"],
        useful_rules["lift"],
        alpha=0.6
    )

    ax2.set_title(
        "Association Rules: Confidence vs Lift"
    )

    ax2.set_xlabel("Confidence")
    ax2.set_ylabel("Lift")

    ax2.grid(True)

    plt.tight_layout()

    st.pyplot(fig2)

    plt.close(fig2)

else:

    st.info(
        "The chart will appear after rules are generated."
    )


# ==========================================
# DOWNLOAD RULES
# ==========================================

st.subheader("⬇️ Export Association Rules")

if len(useful_rules) > 0:

    export_rules = useful_rules.copy()

    export_rules["antecedents"] = (
        export_rules["antecedents"]
        .apply(
            lambda items: ", ".join(
                sorted(items)
            )
        )
    )

    export_rules["consequents"] = (
        export_rules["consequents"]
        .apply(
            lambda items: ", ".join(
                sorted(items)
            )
        )
    )

    csv_data = export_rules.to_csv(
        index=False
    )

    st.download_button(
        label="Download Association Rules CSV",
        data=csv_data,
        file_name="dashboard_association_rules.csv",
        mime="text/csv"
    )


# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.markdown(
    """
    **Project:** Market Basket Analysis

    **Technology:** Python, Pandas, MLxtend,
    Matplotlib, Streamlit

    **Purpose:** Discover purchasing patterns
    for business decision-making.

    **Developed as part of:** Codec Technologies Internship
    """
)