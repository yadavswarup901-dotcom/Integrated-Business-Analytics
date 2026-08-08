
# Integrated Business Analytics & Decision Support System

A VS Code runnable project that combines the four internship tasks into one Data Analytics project.

## Tasks covered

1. **Excel Sales Dashboard**
   - Sales, profit, quantity and category/region analysis
   - Monthly sales trends
   - Top/low performing products

2. **Data Cleaning and Preparation**
   - Python + Pandas
   - Duplicate removal
   - Missing-value handling
   - Data type conversion
   - Derived analytical columns

3. **Interactive Visualization**
   - Streamlit dashboard with interactive filters
   - KPI cards
   - Charts and drill-down style analysis

4. **Marketing Business Insights / EDA**
   - Spend, revenue, conversions
   - CTR, conversion rate, CPC and ROI
   - Channel comparison
   - Spend vs revenue relationship
   - Budget recommendation

## Software required

- Python 3.10 or newer
- VS Code
- Python extension for VS Code

## How to run

Open the project folder in VS Code.

### 1. Create a virtual environment

Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install libraries

```bash
pip install -r requirements.txt
```

### 3. Clean the datasets

```bash
python scripts/data_cleaning.py
```

### 4. Start the dashboard

```bash
streamlit run app.py
```

The browser will open automatically.

## Dataset replacement

The included CSV files are demonstration datasets so the project runs immediately.

To use your actual internship datasets, replace:

- `data/raw/sales.csv`
- `data/raw/marketing.csv`
- `data/raw/hr.csv`

Keep the column names used by the project, or modify the cleaning script to match your files.

## Project flow

Raw CSV → Pandas Cleaning → Cleaned CSV → EDA → Interactive Dashboard → Business Insights

## Suggested viva explanation

"I developed an Integrated Business Analytics and Decision Support System by combining my four internship tasks. I used Python and Pandas for data cleaning and preparation, performed exploratory analysis, and built interactive dashboards using Streamlit and Plotly. The project analyzes sales performance, marketing ROI and employee attrition. The final dashboard allows users to filter the data and obtain business insights for decision-making."

## Important

The sample datasets are synthetic/demo data for development and testing. Replace them with the actual datasets supplied for your internship when available.
