import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Indian Fresher Job Market EDA",
    page_icon="📊",
    layout="wide"
)

@st.cache_data
def load_data():
    df = pd.read_csv('fresher_hiring_india_dataset.csv')
    df.drop(columns=['interview_rounds', 'offered_salary_inr', 'linkedin_premium'], inplace=True, errors='ignore')
    df['application_date'] = pd.to_datetime(df['application_date'], errors='coerce')
    return df

df = load_data()

# ── Sidebar filters ──────────────────────────────────────────────────────────
st.sidebar.header("Filters")

stages = st.sidebar.multiselect(
    "Hiring stage",
    options=df['hiring_stage'].unique(),
    default=df['hiring_stage'].unique()
)

genders = st.sidebar.multiselect(
    "Gender",
    options=df['gender'].unique(),
    default=df['gender'].unique()
)

cgpa_min, cgpa_max = st.sidebar.slider(
    "CGPA range",
    min_value=float(df['cgpa'].min()),
    max_value=float(df['cgpa'].max()),
    value=(float(df['cgpa'].min()), float(df['cgpa'].max())),
    step=0.1
)

work_types = st.sidebar.multiselect(
    "Work type",
    options=df['work_type'].unique(),
    default=df['work_type'].unique()
)

sectors = st.sidebar.multiselect(
    "Sector",
    options=df['sector'].unique(),
    default=df['sector'].unique()
)

# ── Apply filters ────────────────────────────────────────────────────────────
filtered = df[
    df['hiring_stage'].isin(stages) &
    df['gender'].isin(genders) &
    df['cgpa'].between(cgpa_min, cgpa_max) &
    df['work_type'].isin(work_types) &
    df['sector'].isin(sectors)
]

# ── Header ───────────────────────────────────────────────────────────────────
st.title("Indian fresher job market")
st.caption("Who gets hired — and why?")

# ── Metric cards ─────────────────────────────────────────────────────────────
hired = filtered[filtered['hiring_stage'] == 'Offer']
offer_rate = round(len(hired) / len(filtered) * 100, 1) if len(filtered) > 0 else 0
top_sector = filtered['sector'].value_counts().idxmax() if len(filtered) > 0 else "—"

col1, col2, col3, col4 = st.columns(4)
col1.metric("Candidates", f"{len(filtered):,}")
col2.metric("Avg CGPA", f"{filtered['cgpa'].mean():.2f}" if len(filtered) > 0 else "—")
col3.metric("Top sector", top_sector)
col4.metric("Offer rate", f"{offer_rate}%")

st.divider()

# ── Tabs ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Overview", "Academic", "Job roles", "Trends", "Raw data"]
)

def show_fig(fig):
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# ── Tab 1: Overview ───────────────────────────────────────────────────────────
with tab1:
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Hiring stage distribution")
        fig, ax = plt.subplots(figsize=(6, 4))
        order = filtered['hiring_stage'].value_counts().index
        sns.countplot(data=filtered, x='hiring_stage', order=order, ax=ax)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha='right')
        ax.set_xlabel("")
        show_fig(fig)

    with col_b:
        st.subheader("Gender vs hiring stage")
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.countplot(data=filtered, x='hiring_stage', hue='gender', ax=ax)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha='right')
        ax.set_xlabel("")
        show_fig(fig)

    col_c, col_d = st.columns(2)

    with col_c:
        st.subheader("Work type vs hiring stage")
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.countplot(data=filtered, x='work_type', hue='hiring_stage', ax=ax)
        ax.set_xlabel("")
        show_fig(fig)

    with col_d:
        st.subheader("Response time by referral")
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.boxplot(data=filtered, x='referral_applied', y='response_time_days', ax=ax)
        show_fig(fig)

# ── Tab 2: Academic ───────────────────────────────────────────────────────────
with tab2:
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("CGPA distribution")
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.histplot(data=filtered, x='cgpa', bins=20, kde=True, ax=ax)
        show_fig(fig)

    with col_b:
        st.subheader("CGPA by hiring stage")
        fig, ax = plt.subplots(figsize=(6, 4))
        order = filtered['hiring_stage'].value_counts().index
        sns.boxplot(data=filtered, x='hiring_stage', y='cgpa', order=order, ax=ax)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha='right')
        ax.set_xlabel("")
        show_fig(fig)

    col_c, col_d = st.columns(2)

    with col_c:
        st.subheader("Age distribution")
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.histplot(data=filtered, x='age', bins=20, kde=True, ax=ax)
        show_fig(fig)

    with col_d:
        st.subheader("Backlogs vs hiring stage")
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.countplot(data=filtered, x='backlogs', hue='hiring_stage', ax=ax)
        ax.set_xlabel("Has backlogs")
        show_fig(fig)

    st.subheader("Correlation heatmap")
    fig, ax = plt.subplots(figsize=(8, 5))
    corr = filtered.select_dtypes(include='number').corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
    show_fig(fig)

# ── Tab 3: Job roles ──────────────────────────────────────────────────────────
with tab3:
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Top job roles")
        fig, ax = plt.subplots(figsize=(6, 5))
        order = filtered['job_role'].value_counts().head(10).index
        sns.countplot(data=filtered, y='job_role', order=order, ax=ax)
        ax.set_ylabel("")
        show_fig(fig)

    with col_b:
        st.subheader("Branch-wise demand")
        fig, ax = plt.subplots(figsize=(6, 5))
        order = filtered['branch'].value_counts().head(10).index
        sns.countplot(data=filtered, y='branch', order=order, ax=ax)
        ax.set_ylabel("")
        show_fig(fig)

    col_c, col_d = st.columns(2)

    with col_c:
        st.subheader("Sector distribution")
        fig, ax = plt.subplots(figsize=(6, 5))
        order = filtered['sector'].value_counts().index
        sns.countplot(data=filtered, y='sector', order=order, ax=ax)
        ax.set_ylabel("")
        show_fig(fig)

    with col_d:
        st.subheader("Top job locations")
        fig, ax = plt.subplots(figsize=(6, 5))
        order = filtered['job_location'].value_counts().head(10).index
        sns.countplot(data=filtered, y='job_location', order=order, ax=ax)
        ax.set_ylabel("")
        show_fig(fig)

# ── Tab 4: Trends ─────────────────────────────────────────────────────────────
with tab4:
    st.subheader("Year-wise application trend")
    trend = filtered.groupby(filtered['application_date'].dt.year).size()
    fig, ax = plt.subplots(figsize=(9, 4))
    trend.plot(kind='line', marker='o', ax=ax)
    ax.set_xlabel("Year")
    ax.set_ylabel("Applications")
    show_fig(fig)

    st.subheader("Response time by hiring stage")
    fig, ax = plt.subplots(figsize=(9, 4))
    order = filtered['hiring_stage'].value_counts().index
    sns.boxplot(data=filtered, x='hiring_stage', y='response_time_days', order=order, ax=ax)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha='right')
    ax.set_xlabel("")
    show_fig(fig)

# ── Tab 5: Raw data ───────────────────────────────────────────────────────────
with tab5:
    st.subheader(f"Filtered dataset — {len(filtered):,} rows")
    st.dataframe(filtered, use_container_width=True)
    csv = filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download filtered CSV",
        data=csv,
        file_name='filtered_fresher_data.csv',
        mime='text/csv'
    )
