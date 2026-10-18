# SmartGTM — Marketing Analytics Dashboard

SmartGTM is a Python-based marketing analytics dashboard built with Streamlit. It helps users analyze campaign performance, compare marketing channels, monitor key performance indicators (KPIs), and generate rule-based marketing recommendations from uploaded CSV and Excel data.

## Features

- **CSV and Excel Uploads:** Import marketing campaign data in CSV or XLSX format.
- **Data Validation and Cleaning:** Check required columns, handle invalid numeric values, and validate campaign metrics.
- **Interactive Dashboard:** View marketing data in a structured table and filter results by marketing channel.
- **Business Performance KPIs:** Calculate total leads, conversions, conversion rate, cost per lead, cost per conversion, and total marketing spend.
- **Channel Performance Analysis:** Compare conversion rates and acquisition costs across marketing channels.
- **Automated Marketing Recommendations:** Generate rule-based suggestions based on conversion rates, campaign costs, and channels with spending but no recorded conversions.
- **Interactive Visualizations:** Explore leads, conversions, and marketing spend using Plotly charts.
- **Campaign Trend Analysis:** Analyze leads, conversions, and spending over time when a valid `Date` column is available.
- **Report Downloads:** Export the filtered marketing data as CSV or Excel reports.

## Technologies Used

- Python
- Streamlit
- Pandas
- Plotly Express
- OpenPyXL
- Git and GitHub
- Visual Studio Code

## Required Data Format

Upload a CSV or Excel file containing these columns:

| Column | Description |
|---|---|
| `Channel` | Marketing channel name |
| `Leads` | Number of leads generated |
| `Conversions` | Number of recorded conversions |
| `Marketing Spend` | Amount spent on the campaign |

An optional `Date` column enables campaign trend analysis. Ensure dates are valid and numeric fields contain appropriate values.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/manasaarukonda-06/SmartGTM.git
cd SmartGTM
```

Alternatively, download the repository ZIP and extract it.

### 2. Create a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
```

### 3. Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
python -m pip install streamlit pandas plotly openpyxl
```

### 5. Run the dashboard

```powershell
python -m streamlit run app.py
```

### 6. Open the application

Open the local URL displayed in the terminal, typically `http://localhost:8501`.

## How It Works

1. Upload a marketing dataset using the dashboard sidebar.
2. Select the marketing channels you want to analyze.
3. Review overall KPIs and campaign records.
4. Compare channel performance using tables and charts.
5. Review the automated, rule-based marketing recommendations.
6. Analyze campaign trends when date information is available.
7. Download the processed data as a CSV or Excel report.

## Learning Outcomes

This project demonstrates practical experience in:

- Python programming and data manipulation
- Data cleaning and validation
- KPI calculation and business analytics
- Interactive dashboard development
- Data visualization with Plotly
- File handling and report generation
- Rule-based business insights
- Git version control and GitHub collaboration

## Future Improvements

- Add customizable date-range filters
- Support additional business KPIs
- Enhance automated report summaries
- Deploy the dashboard for online access
- Improve recommendations with more advanced analytics

## Disclaimer

SmartGTM is an educational analytics project. Recommendations are based on predefined rules and the data provided by the user. They are intended to support analysis, not replace business judgment. Results depend on the quality and completeness of the uploaded data.