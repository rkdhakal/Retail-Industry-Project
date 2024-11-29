import numpy as np
import pandas as pd
from models.model import PriceOptimizationModel

if __name__ == "__main__":
    # Load data
    final_df = pd.read_csv('data/final_dataset.csv')

    # Initialize and train the model
    model = PriceOptimizationModel()
    model.train(final_df)

    # Evaluate the model
    metrics = model.evaluate()
    print(f"Model Metrics: {metrics}")

    # Optimize price for a specific product
    product_id = 12
    product = final_df[final_df['Product_ID'] == product_id].iloc[0]
    price_range = np.linspace(10, 20, 50)
    optimal_price, max_profit = model.optimize_price(
        product['Product_Cost'], price_range)

    print(f"Optimal Price: ${
          optimal_price:.2f}, Maximum Profit: ${max_profit:.2f}")
