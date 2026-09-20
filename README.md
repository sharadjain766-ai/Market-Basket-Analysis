# 🛒 Market Basket Analysis

## Internship Project

This project was developed as part of my internship at **Codec
Technologies**.

The project uses **Market Basket Analysis** to identify products that
customers frequently purchase together. The Apriori algorithm and
association rules are used to discover useful purchasing patterns.

## Project Objective

-   Identify frequently purchased product combinations.
-   Generate association rules using the Apriori algorithm.
-   Analyze support, confidence, and lift.
-   Display insights through a Streamlit dashboard.
-   Export association rules as a CSV file.

## Technologies Used

-   Python
-   Pandas
-   Matplotlib
-   MLxtend
-   Streamlit
-   Excel dataset processing

## Project Structure

``` text
Market_Basket_Analysis/
│
├── Market_Basket_Analysis.ipynb
├── Online Retail.xlsx
├── association_rules.csv
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Dataset

The project uses the **Online Retail** dataset in Excel format.

The dataset contains transaction-level information such as:

-   Invoice number
-   Product description
-   Quantity
-   Customer purchasing records

## Data Cleaning

The following preprocessing steps were performed:

1.  Removed missing invoice numbers and product descriptions.
2.  Removed cancelled transactions.
3.  Removed zero and negative quantities.
4.  Selected the 150 most frequently purchased products for dashboard
    processing.
5.  Converted transaction data into a binary basket format.

## Methodology

### 1. Exploratory Data Analysis

The dataset was inspected using:

-   Dataset shape
-   Column information
-   Missing value analysis
-   Descriptive statistics
-   Product quantity analysis

### 2. Transaction Basket

Each row represents an invoice, and each column represents a product.

A value of:

-   `1` means the product was purchased in that transaction.
-   `0` means the product was not purchased.

### 3. Apriori Algorithm

The Apriori algorithm was used to generate frequent itemsets.

The dashboard uses:

-   Configurable minimum support
-   Maximum itemset length of 2
-   Memory-efficient processing

### 4. Association Rules

Association rules were generated using:

-   Support
-   Confidence
-   Lift

Rules with lift greater than 1 were treated as useful association rules
for analysis.

## Dashboard Features

The Streamlit dashboard includes:

-   Dataset overview KPI cards
-   Total transactions
-   Number of products analyzed
-   Number of frequent itemsets
-   Number of useful association rules
-   Top 10 products by quantity sold
-   Frequent itemsets table
-   Association rules table
-   Confidence versus lift scatter plot
-   Downloadable CSV export
-   Sidebar controls for support and confidence

## How to Run the Project

### Step 1: Download or Clone the Repository

``` bash
git clone YOUR_GITHUB_REPOSITORY_LINK
cd Market_Basket_Analysis
```

### Step 2: Install Required Libraries

``` bash
pip install -r requirements.txt
```

### Step 3: Start the Streamlit Dashboard

``` bash
python -m streamlit run app.py
```

The dashboard will open in your browser at a local address similar to:

``` text
http://localhost:8501
```

### Step 4: Run the Jupyter Notebook

Open JupyterLab or Jupyter Notebook and open:

``` text
Market_Basket_Analysis.ipynb
```

## Example Results

During dashboard testing, the project generated:

-   16,864 transactions
-   150 analyzed products
-   286 frequent itemsets
-   213 useful association rules

These values can change if the dataset or dashboard settings are
changed.

## Business Applications

Market Basket Analysis can support:

-   Product bundling
-   Cross-selling recommendations
-   Store layout planning
-   Inventory planning
-   Promotional offers
-   Customer purchasing pattern analysis

## Limitations

-   The dashboard analyzes the 150 most frequently purchased products to
    reduce memory usage.
-   The current implementation focuses on product pairs.
-   Association does not necessarily mean causation.
-   Results depend on support and confidence settings.

## Future Improvements

-   Add product recommendation functionality.
-   Add date-wise sales analysis.
-   Add customer segmentation.
-   Deploy the dashboard online.
-   Use larger-scale processing techniques for the complete product
    catalog.

## Author

**Sharad Jain**

B.Tech CSE (Data Science)

Project completed as part of the **Codec Technologies Internship**.
