import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the datasets
medal_df = pd.read_csv("Olympics 2024 Medals Table.csv")
competition_df = pd.read_csv("Olympics 2024.csv")

# Streamlit App Layout
st.title("Olympics 2024 Medal Analysis")

# Sidebar for navigation
st.sidebar.image("o_logo.png", use_column_width=True)
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Medal Analysis", "Competitions Analysis"])

# Medal Analysis Section
if section == "Medal Analysis":
    st.write("### Olympics Medal Table")
    st.dataframe(medal_df)

    # Basic Statistics and Rankings
    st.write("## Basic Statistics and Rankings")
    st.write("#### Total Medal Count by Country")
    st.bar_chart(medal_df.set_index('TEAM')['TOTAL'])

    # Medal Proportions
    st.write("#### Medal Proportions for Each Country")
    medal_df['Gold %'] = medal_df['GOLD'] / medal_df['TOTAL'] * 100
    medal_df['Silver %'] = medal_df['SILVER'] / medal_df['TOTAL'] * 100
    medal_df['Bronze %'] = medal_df['BRONZE'] / medal_df['TOTAL'] * 100

    fig, ax = plt.subplots(figsize=(10, 6))
    medal_df.set_index('TEAM')[['Gold %', 'Silver %', 'Bronze %']].plot(kind='bar', stacked=True, ax=ax)
    ax.set_ylabel("Percentage")
    ax.set_xticklabels(medal_df['TEAM'], rotation=90, ha='right', fontsize=10)
    st.pyplot(fig)

    # Country Comparison
    st.write("## Compare Countries")
    selected_countries = st.multiselect("Select Countries to Compare", medal_df['TEAM'].unique(), default=medal_df['TEAM'].unique()[0:2])
    comparison_df = medal_df[medal_df['TEAM'].isin(selected_countries)]
    st.bar_chart(comparison_df.set_index('TEAM')[['GOLD', 'SILVER', 'BRONZE']])

    # Correlation Analysis
    st.write("## Correlation Between Medal Types")
    corr = medal_df[['GOLD', 'SILVER', 'BRONZE']].corr()
    sns.heatmap(corr, annot=True, cmap="coolwarm")
    st.pyplot(plt)

    # Country and Medal-wise Analysis
    st.write("## Country and Medal-wise Analysis")
    country = st.selectbox("Select a Country for Detailed Analysis", medal_df['TEAM'].unique())
    country_data = medal_df[medal_df['TEAM'] == country]
    fig, ax = plt.subplots()
    ax.pie(
        [country_data['GOLD'].values[0], country_data['SILVER'].values[0], country_data['BRONZE'].values[0]],
        labels=['Gold', 'Silver', 'Bronze'], autopct='%1.1f%%', colors=['#FFD700', '#C0C0C0', '#CD7F32']
    )
    st.pyplot(fig)

    # Medal-wise Analysis
    medal_type = st.selectbox("Select Medal Type for Analysis", ['GOLD', 'SILVER', 'BRONZE'])
    top_countries = medal_df.sort_values(by=medal_type, ascending=False).head(10)
    st.bar_chart(top_countries.set_index('TEAM')[medal_type])

    # Static Analysis - Summary Statistics
    st.write("## Static Analysis - Summary Statistics")
    st.write("#### Total Medals Overview")
    st.write(medal_df[['GOLD', 'SILVER', 'BRONZE', 'TOTAL']].sum())

    st.write("#### Top Countries by Medal Type")
    top_gold = medal_df[medal_df['GOLD'] == medal_df['GOLD'].max()]['TEAM'].values[0]
    top_silver = medal_df[medal_df['SILVER'] == medal_df['SILVER'].max()]['TEAM'].values[0]
    top_bronze = medal_df[medal_df['BRONZE'] == medal_df['BRONZE'].max()]['TEAM'].values[0]
    st.write(f"Top Gold Medal Winner: {top_gold}")
    st.write(f"Top Silver Medal Winner: {top_silver}")
    st.write(f"Top Bronze Medal Winner: {top_bronze}")

# Competitions Analysis Section
elif section == "Competitions Analysis":
    st.write("### Olympics Competitions Dataset")
    st.dataframe(competition_df)

    # Analysis 1: Competition-Wise Medal Distribution
    st.write("## Competition-Wise Medal Distribution")
    selected_competition = st.selectbox("Select Competition", competition_df['Competitions'].unique())
    comp_data = competition_df[competition_df['Competitions'] == selected_competition]

    fig, ax = plt.subplots()
    comp_data.set_index('NOC')[['Gold', 'Silver', 'Bronze']].plot(kind='bar', stacked=True, ax=ax)
    ax.set_ylabel("Medal Count")
    ax.set_title(f"Medal Distribution in {selected_competition}")
    ax.set_xticklabels(comp_data['NOC'], rotation=45, ha='right')
    st.pyplot(fig)

    # Analysis 2: Top Performing Countries in Each Competition
    st.write("## Top Performing Countries in Each Competition")
    top_performing = comp_data.sort_values(by='Total', ascending=False).head(3)
    st.write(f"### Top 3 Countries in {selected_competition}")
    st.dataframe(top_performing[['Rank', 'NOC', 'Gold', 'Silver', 'Bronze', 'Total']])

    # Analysis 3: Country-Wise Performance Across Competitions
    st.write("## Country-Wise Performance Across Competitions")
    selected_country = st.selectbox("Select Country", competition_df['NOC'].unique())
    country_data = competition_df[competition_df['NOC'] == selected_country]

    fig, ax = plt.subplots()
    country_data.set_index('Competitions')[['Gold', 'Silver', 'Bronze']].plot(kind='bar', ax=ax)
    ax.set_ylabel("Medal Count")
    ax.set_title(f"{selected_country}'s Performance Across Competitions")
    ax.set_xticklabels(country_data['Competitions'], rotation=45, ha='right')
    st.pyplot(fig)

    # Analysis 4: Medal Efficiency
    st.write("## Medal Efficiency by Country")
    efficiency_data = competition_df.groupby('NOC').sum().reset_index()
    efficiency_data['Efficiency'] = efficiency_data['Total'] / efficiency_data['Total'].sum() * 100

    fig, ax = plt.subplots()
    sns.barplot(x='NOC', y='Efficiency', data=efficiency_data, ax=ax)
    ax.set_ylabel("Efficiency (%)")
    ax.set_xticklabels(efficiency_data['NOC'], rotation=90, ha='right')
    st.pyplot(fig)

    # Analysis 5: Comparison Between Competitions
    st.write("## Comparison Between Competitions")
    competition_totals = competition_df.groupby('Competitions')['Total'].sum().reset_index()

    fig, ax = plt.subplots()
    sns.barplot(x='Competitions', y='Total', data=competition_totals, ax=ax)
    ax.set_ylabel("Total Medals")
    ax.set_xticklabels(competition_totals['Competitions'], rotation=90, ha='right')
    st.pyplot(fig)

    # # Analysis 6: Correlation Between Medal Types
    # st.write("## Correlation Between Medal Types")
    # medal_corr = competition_df[['Gold', 'Silver', 'Bronze']].corr()
    # fig, ax = plt.subplots()
    # sns.heatmap(medal_corr, annot=True, cmap="coolwarm", ax=ax)
    # ax.set_title("Correlation Between Medal Types")
    # st.pyplot(fig)

    # Country Details and Interaction
    st.write("## Country Details and Interaction")
    country_detail = st.selectbox("Select a Country for Detailed Analysis", competition_df['NOC'].unique())
    detail_data = competition_df[competition_df['NOC'] == country_detail]
    st.write(f"### Detailed Performance of {country_detail}")
    st.dataframe(detail_data[['Competitions', 'Rank', 'Gold', 'Silver', 'Bronze', 'Total']])
