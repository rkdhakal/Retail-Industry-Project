import pytest
from models.model import PriceOptimizationModel
import pandas as pd


@pytest.fixture
def sample_data():
    return pd.DataFrame({
        "Product_Cost": [10, 12, 14],
        "Product_Price": [15, 18, 20],
        "Units": [100, 80, 60]
    })


def test_model_training(sample_data):
    model = PriceOptimizationModel()
    model.train(sample_data)
    metrics = model.evaluate()
    assert "mse" in metrics
    assert "r2" in metrics
