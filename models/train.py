import pandas as pd
from models.model import PriceOptimizationModel

def load_data(file_path):
    return pd.read_csv(file_path)

if __name__ == "__main__":
    # Load dataset
    final_df = load_data('data/final_dataset.csv')

    # Initialize and train the model
    model = PriceOptimizationModel()
    model.train(final_df)

    # Evaluate model performance
    metrics = model.evaluate()
    print(f"Model Metrics: {metrics}")
