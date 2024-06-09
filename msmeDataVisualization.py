import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor

# Load the dataset
def load_data():
    data = pd.read_csv('msme_dataset.csv')
    data = data.drop(columns=['Sl.no.','company_name'])
    return data

# Define the target column
target_column = 'target'

# Train the model
def train_model(data):
    X = data.drop(columns=['target'])
    y = data['target']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = GradientBoostingRegressor()
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    
    return model

def main():
    st.header("Data Visualization")

    # Load data
    data = load_data()

    # Train model and display MSE
    model = train_model(data)

    # Plot distribution of BPSRI scores
    st.subheader("Distribution of BPSRI Scores")
    fig = px.histogram(data, x='target', nbins=50, title='Distribution of BPSRI Scores')
    st.plotly_chart(fig)
    
    # Pair plot
    if target_column in data.columns:
        st.subheader("Pair Plot")

        # Exclude the target column from the features for selection
        available_features = list(data.columns)
        available_features.remove(target_column)

        # Create a multiselect widget for feature selection
        selected_features = st.multiselect("Select features for pair plot", available_features, default=available_features[:5])

        if len(selected_features) > 1:
            # Create the pair plot with the selected features and 'target'
            fig = sns.pairplot(data[selected_features + [target_column]])
        
            # Display the plot in the Streamlit app
            st.pyplot(fig)
        else:
            st.write("Please select at least two features to generate a pair plot.")
    else:
        st.write(f"Target column '{target_column}' does not exist in the DataFrame.")
    
    # Feature importance
    st.subheader("Feature Importance")
    feature_importance = pd.Series(model.feature_importances_, index=data.columns[:-1]).sort_values(ascending=False)
    fig = px.bar(feature_importance, title="Feature Importance")
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()
