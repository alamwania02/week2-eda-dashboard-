from matplotlib import pyplot as plt
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns

# PAGE CONFIG

st.set_page_config(
    page_title="Student Performance Analytics Dashboard",
    layout="wide"
)
# LOAD DATA

df = pd.read_csv("student-scores.csv")

# HANDLE MISSING VALUES
numeric_cols = df.select_dtypes(include=np.number).columns
df[numeric_cols] = df[numeric_cols].fillna(
    df[numeric_cols].mean()
)

categorical_cols = df.select_dtypes(exclude=np.number).columns

for col in categorical_cols:
    df[col] = df[col].fillna(
        df[col].mode()[0]
    )

# DATA CLEANING
rows_before = len(df)

duplicates_removed = df.duplicated().sum()
df.drop_duplicates(inplace=True)

score_columns = [
    "math_score",
    "history_score",
    "physics_score",
    "chemistry_score",
    "biology_score",
    "english_score",
    "geography_score"
]

df["average_score"] = df[score_columns].mean(axis=1)

# OUTLIER HANDLING
Q1 = df["average_score"].quantile(0.25)
Q3 = df["average_score"].quantile(0.75)

IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers_removed = len(
    df[
        (df["average_score"] < lower_bound)
        |
        (df["average_score"] > upper_bound)
    ]
)

df = df[
    (df["average_score"] >= lower_bound)
    &
    (df["average_score"] <= upper_bound)
]

rows_after = len(df)

# SIDEBAR FILTERS
st.sidebar.title(" Filters")

gender_filter = st.sidebar.selectbox(
    "Gender",
    ["All"] + sorted(df["gender"].unique())
)

career_filter = st.sidebar.selectbox(
    "Career Aspiration",
    ["All"] + sorted(df["career_aspiration"].unique())
)

filtered_df = df.copy()

if gender_filter != "All":
    filtered_df = filtered_df[
        filtered_df["gender"] == gender_filter
    ]

if career_filter != "All":
    filtered_df = filtered_df[
        filtered_df["career_aspiration"] == career_filter
    ]

# TITLE
st.title("Student Performance Analytics Dashboard")


st.divider()
# KPI CARDS
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Students",
    len(filtered_df)
)

col2.metric(
    "Average Score",
    round(filtered_df["average_score"].mean(), 2)
)

col3.metric(
    "Study Hours",
    round(
        filtered_df["weekly_self_study_hours"].mean(),
        2
    )
)

col4.metric(
    "Absence Days",
    round(
        filtered_df["absence_days"].mean(),
        2
    )
)

st.divider()

# TABS
tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Overview",
        "Statistics",
        "Visualizations",
        "Insights"
    ]
)
with tab1:

    st.subheader("Dataset Preview")

    st.dataframe(filtered_df.head(10))

    st.subheader("Data Cleaning Summary")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Rows Before Cleaning",
        rows_before
    )

    c2.metric(
        "Rows After Cleaning",
        rows_after
    )

    c3.metric(
        "Duplicates Removed",
        duplicates_removed
    )

    c4.metric(
        "Outliers Removed",
        outliers_removed
    )

    st.subheader("Missing Values")

    st.dataframe(
        filtered_df.isnull()
        .sum()
        .reset_index()
        .rename(
            columns={
                "index": "Column",
                0: "Missing Values"
            }
        )
    )

# TAB 2 : STATISTICS
with tab2:

    st.subheader("Statistical Summary")

    st.dataframe(
        filtered_df.describe()
    )

# TAB 3 : VISUALIZATIONS
with tab3:

    # Average Score Distribution
    fig1 = px.histogram(
        filtered_df,
        x="average_score",
        nbins=25,
        title="Distribution of Average Scores"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    # Gender Performance
    gender_avg = (
        filtered_df.groupby("gender")
        ["average_score"]
        .mean()
        .reset_index()
    )

    fig2 = px.bar(
        gender_avg,
        x="gender",
        y="average_score",
        text_auto=".2f",
        title="Average Score by Gender"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    # Study Hours vs Score
    fig3 = px.scatter(
        filtered_df,
        x="weekly_self_study_hours",
        y="average_score",
        color="gender",
        title="Study Hours vs Average Score"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    # Absence Days
    fig4 = px.histogram(
        filtered_df,
        x="absence_days",
        title="Distribution of Absence Days"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

    # Career Aspirations
    career_counts = (
        filtered_df["career_aspiration"]
        .value_counts()
        .sort_values()
        .reset_index()
    )

    career_counts.columns = [
        "Career",
        "Count"
    ]

    fig5 = px.bar(
        career_counts,
        x="Count",
        y="Career",
        orientation="h",
        text="Count",
        title="Career Aspiration Distribution"
    )

    fig5.update_layout(height=650)

    st.plotly_chart(
        fig5,
        use_container_width=True
    )

    # Part Time Job Impact
    fig6 = px.box(
        filtered_df,
        x="part_time_job",
        y="average_score",
        title="Part-Time Job Impact on Academic Performance"
    )

    st.plotly_chart(
        fig6,
        use_container_width=True
    )
    # CORRELATION HEATMAP
    st.subheader("Correlation Heatmap")

    heatmap_df = filtered_df[
        [
            "weekly_self_study_hours",
            "absence_days",
            "math_score",
            "physics_score",
            "english_score",
            "average_score"
        ]
    ].copy()

    heatmap_df.columns = [
        "Study Hours",
        "Absences",
        "Math",
        "Physics",
        "English",
        "Avg Score"
    ]

    corr = heatmap_df.corr()

    fig, ax = plt.subplots(
        figsize=(10,7)
    )

    sns.heatmap(
        corr,
        annot=True,
        fmt=".2f",
        cmap="YlGnBu",
        linewidths=0.1,
        square=True,
        cbar=True,
        annot_kws={"size": 10}
    )

    ax.set_title(
        "Student Performance Correlations",
        fontsize= 8,
        pad=10
    )

    plt.xticks(
        rotation = 0
    )

    plt.yticks(
        rotation=0
    )

    st.pyplot(fig)

# TAB 4 : INSIGHTS
with tab4:

    st.subheader("Top 10 Students")

    top_students = (
        filtered_df
        .sort_values(
            "average_score",
            ascending=False
        )
        .head(10)
    )

    st.dataframe(
        top_students[
            [
                "first_name",
                "last_name",
                "average_score",
                "career_aspiration"
            ]
        ]
    )

    st.subheader("Insights & Findings")

    st.markdown("""
### Key Findings

- Students with higher self-study hours generally achieve better academic performance.
- Higher absence days tend to lower academic scores.
- Math, Physics and English scores are positively correlated.
- Academic subjects have a strong relationship with overall performance.
- Career aspirations vary significantly across students.
- Part-time jobs show only a small impact on overall academic outcomes.
""")

    st.subheader("Download Cleaned Dataset")

    csv = filtered_df.to_csv(index=False)

    st.download_button(
        label="Download Cleaned Dataset",
        data=csv,
        file_name="cleaned_student_scores.csv",
        mime="text/csv"
    )