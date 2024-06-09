import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from msmeDataVisualization import main as main_file1
from msmeDashboard import main as main_file2
from settings import main as main_file3
from msmeGemini_AI import main as main_file4
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error

# Load the dataset
@st.cache_data
def load_data():
    data = pd.read_csv('msme_dataset.csv')
    data = data.drop(columns=['Sl.no.', 'company_name'])
    return data

# Train the model
def train_model(data):
    X = data.drop(columns=['target'])
    y = data['target']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = GradientBoostingRegressor()
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    
    return model, mse

# Predict the target variable
def predict(model, input_data):
    return model.predict([input_data])[0]

# Main Streamlit app
def main():

    # Sidebar setup
    with st.sidebar:
        selected = option_menu(
            menu_title = "Your Suite",
            options = ["BPSRI Prediction","Dashboard", "Infographics","AI Analysis/Feedback", "Settings"],
            icons = ["buildings-fill","bar-chart-line-fill","bar-chart-steps","bullseye","gear-wide-connected"],
            menu_icon = ["building-fill-gear"],
            default_index=0,
        )
    
    if selected == "BPSRI Prediction":

        st.title("MSME BPSRI Prediction")
        st.header("Business Performance, Sustainability, and Risk Index (BPSRI):")
        st.write("The BPSRI is a comprehensive metric designed to evaluate the overall health and performance of small to medium-sized enterprises (SMEs). This index aggregates various dimensions of business operations, including financial health, market position, operational efficiency, management quality, customer satisfaction, innovation potential, human resources, risk management, sustainability, and technology. The BPSRI score ranges from 50 to 100, with higher scores indicating better overall business health and lower risks.")
        st.subheader("Please complete the form")
        # Load data
        data = load_data()
    
        st.header("Input Features")

        # Define the keys for session state
        slider_keys = [
            "Revenue Growth", "Profit Margins", "Cash Flow", "Debt Levels", "Liquidity",
            "Market Share", "Competitive Advantage", "Brand Recognition",
            "Productivity", "Supply Chain Efficiency", "Cost Management",
            "Management Experience", "Vision and Strategy", "Corporate Governance",
            "Customer Satisfaction", "Customer Retention", "Market Reach",
            "R&D Investment", "Product Pipeline", "Scalability",
            "Employee Satisfaction", "Talent Acquisition", "Training and Development",
            "Operational Risks", "Compliance", "Insurance",
            "Environmental Impact", "Social Responsibility", "Ethical Practices",
            "IT Infrastructure", "Digital Presence", "Cybersecurity"
        ]

        # Initialize session state for sliders if not already done
        if 'sliders' not in st.session_state:
            st.session_state.sliders = {key: 5.0 for key in slider_keys}
    
        # Initialize session state for tab index and predicted value
        if 'tab_index' not in st.session_state:
            st.session_state.tab_index = 0
    
        if 'predicted_value' not in st.session_state:
            st.session_state.predicted_value = None

        tab_labels = [
            "1. FINANCIAL HEALTH", "2. MARKET POSITION", "3. OPERATIONAL EFFICIENCY", 
            "4. MANAGEMENT", "5. CUSTOMER METRICS", "6. INNOVATION GROWTH", 
            "7. HUMAN RESOURCES", "8. RISK MANAGEMENT", "9. SUSTAINABILITY", 
            "10. TECHNOLOGY & DIGITIZATION"
        ]

        slider_indices = [
            range(5), range(5, 8), range(8, 11), range(11, 14), range(14, 17),
            range(17, 20), range(20, 23), range(23, 26), range(26, 29), range(29, 32)
        ]

        # Display the current tab
        current_tab_label = tab_labels[st.session_state.tab_index]
        st.subheader(current_tab_label)

        # Display sliders for the current tab
        indices = slider_indices[st.session_state.tab_index]
        for i in indices:
            key = slider_keys[i]
            st.session_state.sliders[key] = st.slider(
                key, 1.0, 10.0, st.session_state.sliders[key]
            )

        # Navigation buttons
        col1, col2, col3 = st.columns([1, 2, 1])

        # Update tab_index based on button presses
        if col1.button("Previous") and st.session_state.tab_index > 0:
            st.session_state.tab_index -= 1
            st.experimental_rerun()

        if col3.button("Next") and st.session_state.tab_index < len(tab_labels) - 1:
            st.session_state.tab_index += 1
            st.experimental_rerun()
    
        # Display the Predict button only on the last tab
        if st.session_state.tab_index == len(tab_labels) - 1:
            with col3:
                if st.button("Predict BPSRI"):
                    input_data = [st.session_state.sliders[key] for key in slider_keys]
                    model, mse = train_model(data)
                    st.session_state.predicted_value = predict(model, input_data)
                    st.session_state.model_mse = mse

        # Display the predicted value if it exists
        if st.session_state.predicted_value is not None:
            st.write(f"Predicted BPSRI: {st.session_state.predicted_value:.2f}")
            st.write(f"Model Mean Squared Error: {st.session_state.model_mse}")

    elif selected == "Dashboard":

        main_file2()    

    elif selected == "Infographics":

        main_file1()

    elif selected == "AI Analysis/Feedback":

        main_file4()
    
    elif selected == "Settings":
        main_file3()


if __name__ == "__main__":
    main()
