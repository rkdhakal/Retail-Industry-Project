import streamlit as st
import pandas as pd
import numpy as np
from models.model import PriceOptimizationModel

# Load dataset


@st.cache
def load_data(file_path):
    return pd.read_csv(file_path)

# Streamlit app


def main():
    st.title("Retail Price Optimization Dashboard")
    st.write("Use this dashboard to explore and optimize product pricing.")

    # Load and display data
    st.sidebar.header("Upload Dataset")
    uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])
    if uploaded_file:
        final_df = pd.read_csv(uploaded_file)
        st.write("Dataset Preview:")
        st.dataframe(final_df.head())

        # Train model
        st.sidebar.subheader("Model Configuration")
        n_estimators = st.sidebar.slider(
            "Number of Trees in Random Forest", 10, 200, 100)
        random_state = st.sidebar.number_input("Random State", value=42)

        if st.sidebar.button("Train Model"):
            st.write("Training model...")
            model = PriceOptimizationModel(
                n_estimators=n_estimators, random_state=random_state)
            model.train(final_df)
            metrics = model.evaluate()
            st.success("Model trained successfully!")
            st.write("Model Performance:")
            st.write(f"Mean Squared Error: {metrics['mse']:.2f}")
            st.write(f"R-squared: {metrics['r2']:.2f}")

        # Price optimization
        st.header("Optimize Product Pricing")
        product_id = st.selectbox(
            "Select Product ID", final_df["Product_ID"].unique())
        product = final_df[final_df["Product_ID"] == product_id].iloc[0]

        st.write(f"Selected Product: {product['Product_Name']}")
        price_range = np.linspace(10, 20, 50)
        model = PriceOptimizationModel(
            n_estimators=n_estimators, random_state=random_state)
        model.train(final_df)
        optimal_price, max_profit = model.optimize_price(
            product['Product_Cost'], price_range)

        st.write(f"Optimal Price: ${optimal_price:.2f}")
        st.write(f"Maximum Profit: ${max_profit:.2f}")

        # Profit visualization
        st.subheader("Profit Visualization")
        profits = [(price - product['Product_Cost']) * model.predict_units(
            product['Product_Cost'], price) for price in price_range]

        st.line_chart({"Price": price_range, "Profit": profits})
        st.success(f"Optimal Price is marked at ${optimal_price:.2f}")


if __name__ == "__main__":
    main()
