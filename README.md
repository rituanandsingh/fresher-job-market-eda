# Indian Fresher Job Market — EDA Dashboard

An interactive Streamlit dashboard exploring hiring outcomes for fresh graduates in India: hiring funnel stages, CGPA vs outcome, gender breakdown, branch/sector demand, response times, and year-over-year application trends.

## Live demo
_Add your Streamlit Cloud link here once deployed._

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Make sure `fresher_hiring_india_dataset.csv` is in the same folder as `app.py`.

## Dataset
The dataset contains fresher job applications with fields including `hiring_stage`, `gender`, `age`, `cgpa`, `backlogs`, `college`, `degree`, `branch`, `sector`, `job_role`, `work_type`, `job_location`, `response_time_days`, `referral_applied`, and `application_date`.

## Features
- Sidebar filters: hiring stage, gender, CGPA range, work type, sector
- Overview, Academic, Job roles, Trends, and Raw data tabs
- Correlation heatmap of numeric features
- CSV export of filtered data

## Tech stack
Python, pandas, matplotlib, seaborn, Streamlit
