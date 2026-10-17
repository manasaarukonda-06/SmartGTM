
# SmartGTM — Marketing Analytics Dashboard

SmartGTM is a Python-based marketing analytics dashboard built with Streamlit. It helps users analyze campaign performance, compare marketing channels, and explore business metrics using uploaded CSV and Excel files.

## Features

- Upload CSV and Excel campaign data
- View marketing data in an interactive table
- Filter results by marketing channel
- Track total leads and conversions
- Calculate conversion rate and cost per lead
- Compare cost per conversion across channels
- Visualize leads, conversions, and marketing spend
- Explore campaign trends over time when date data is available
- Download filtered reports as CSV or Excel

## Technologies Used

- Python
- Streamlit
- Pandas
- Plotly
- OpenPyXL
- Visual Studio Code
- Git and GitHub

## Required Data Columns

Your uploaded file should contain these columns:

| Column | Description |
|---|---|
| Channel | Marketing channel name |
| Leads | Number of leads generated |
| Conversions | Number of recorded conversions |
| Marketing Spend | Amount spent on the campaign |

An optional `Date` column enables campaign trend analysis.

## Installation and Setup

1. Clone or download this repository.
2. Open the project folder in VS Code.
3. Create and activate a virtual environment.

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

4. Install the required packages:

```powershell
python -m pip install streamlit pandas plotly openpyxl
```

5. Start the dashboard:

```powershell
python -m streamlit run app.py
```

6. Open the local URL shown in the terminal.

## Project Structure

```text
SmartGTM/
├── app.py
├── main.py
├── README.md
└── .gitignore
```

## Learning Outcomes

This project demonstrates practical skills in data cleaning, data aggregation, KPI calculation, interactive visualization, file handling, and dashboard development.

## Future Improvements

- Add more flexible date filters
- Support customizable business KPIs
- Add automated report summaries
- Improve data validation and error handling

## Disclaimer

SmartGTM is an educational analytics project. Results depend on the quality and completeness of the uploaded data.
