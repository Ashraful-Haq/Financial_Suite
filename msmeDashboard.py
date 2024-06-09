import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def main():
    # Load the dataset
    file_path = 'msme_dataset.csv'  # Ensure this is the correct path
    dataset = pd.read_csv(file_path)

    # Set up the Streamlit app
    st.title("MSME Dataset Dashboard")

    # Sidebar for navigation
    st.sidebar.title("Dashboard Navigation")
    options = st.sidebar.radio("Select a section:", ["Overview", "Visualizations"])

    # Overview Section
    if options == "Overview":
        st.header("Dataset Overview")
        st.write(dataset.head())

        st.header("Summary Statistics")
        st.write(dataset.describe())

    # Visualizations Section
    elif options == "Visualizations":
        st.header("Visualizations")

        # Financial Health Boxplots
        st.subheader("Financial Health")
        financial_health_cols = [
            'financial_health_revenue_growth', 'financial_health_profit_margins',
            'financial_health_cash_flow', 'financial_health_debt_levels',
            'financial_health_liquidity'
        ]
        st.write("### Financial Health Metrics")
        fig, ax = plt.subplots()
        sns.boxplot(data=dataset[financial_health_cols])
        plt.xticks(rotation=90)
        st.pyplot(fig)

        # Market Position Bar Charts
        st.subheader("Market Position")
        market_position_cols = [
            'market_position_market_share', 'market_position_competitive_advantage',
            'market_position_brand_recognition'
        ]
        for col in market_position_cols:
            st.write(f"### {col.replace('_', ' ').title()}")
            fig, ax = plt.subplots()
            sns.barplot(x=dataset.index, y=dataset[col])
            st.pyplot(fig)

        # Operational Efficiency Heatmap
        st.subheader("Operational Efficiency")
        operational_efficiency_cols = [
            'operational_efficiency_productivity', 'operational_efficiency_supply_chain_efficiency',
            'operational_efficiency_cost_management'
        ]
        st.write("### Operational Efficiency Correlation Heatmap")
        fig, ax = plt.subplots()
        sns.heatmap(dataset[operational_efficiency_cols].corr(), annot=True, cmap='coolwarm')
        st.pyplot(fig)

        # Management Leadership Radar Chart
        st.subheader("Management Leadership")
        management_leadership_cols = [
            'management_leadership_experience', 'management_leadership_vision_strategy',
            'management_leadership_corporate_governance'
        ]
        st.write("### Management Leadership Metrics")
        fig, ax = plt.subplots()
        radar_data = dataset[management_leadership_cols].mean()
        categories = list(radar_data.index)
        values = radar_data.values.flatten().tolist()
        values += values[:1]
        angles = [n / float(len(categories)) * 2 * 3.141592653589793 for n in range(len(categories))]
        angles += angles[:1]
        ax = plt.subplot(111, polar=True)
        plt.xticks(angles[:-1], categories)
        ax.plot(angles, values)
        ax.fill(angles, values, 'teal', alpha=0.1)
        st.pyplot(fig)

        # Customer Metrics Line Chart
        st.subheader("Customer Metrics")
        customer_metrics_cols = [
            'customer_metrics_customer_satisfaction', 'customer_metrics_customer_retention',
            'customer_metrics_market_reach'
        ]
        for col in customer_metrics_cols:
            st.write(f"### {col.replace('_', ' ').title()}")
            fig, ax = plt.subplots()
            plt.plot(dataset[col])
            st.pyplot(fig)

        # Innovation & Growth Scatter Plots
        st.subheader("Innovation & Growth")
        innovation_growth_cols = [
            'innovation_growth_RnD_investment', 'innovation_growth_product_pipeline',
            'innovation_growth_scalability'
        ]
        for col in innovation_growth_cols:
            st.write(f"### {col.replace('_', ' ').title()}")
            fig, ax = plt.subplots()
            plt.scatter(dataset.index, dataset[col])
            st.pyplot(fig)

        # Human Resources Histograms
        st.subheader("Human Resources")
        human_resources_cols = [
            'human_resources_employee_satisfaction', 'human_resources_talent_acquisition',
            'human_resources_training_development'
        ]
        for col in human_resources_cols:
            st.write(f"### {col.replace('_', ' ').title()}")
            fig, ax = plt.subplots()
            plt.hist(dataset[col], bins=20)
            st.pyplot(fig)

        # Sustainability Bar Charts
        st.subheader("Sustainability")
        sustainability_cols = [
            'sustainability_social_environmental_impact', 'sustainability_social_ethical_practices'
        ]
        for col in sustainability_cols:
            st.write(f"### {col.replace('_', ' ').title()}")
            fig, ax = plt.subplots()
            sns.barplot(x=dataset.index, y=dataset[col])
            st.pyplot(fig)

        # Technology & Digitalization Box Plots
        st.subheader("Technology & Digitalization")
        technology_cols = [
            'technology_digitalization_IT_infrastructure', 'technology_digitalization_digital_presence',
            'technology_digitalization_cybersecurity'
        ]
        st.write("### Technology & Digitalization Metrics")
        fig, ax = plt.subplots()
        sns.boxplot(data=dataset[technology_cols])
        plt.xticks(rotation=90)
        st.pyplot(fig)

        # Target Variable Analysis
        st.subheader("BPSRI (Business Performance, Sustainability, and Risk Index) Analysis")
        st.write("### BPSRI Distribution")
        fig, ax = plt.subplots()
        sns.histplot(dataset['target'], bins=20, kde=True)
        st.pyplot(fig)

        st.write("### Relationship with Financial Health Revenue Growth")
        fig, ax = plt.subplots()
        sns.scatterplot(x=dataset['financial_health_revenue_growth'], y=dataset['target'])
        st.pyplot(fig)

if __name__ == "__main__":
    main()

