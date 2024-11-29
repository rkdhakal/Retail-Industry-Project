import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

class PriceOptimizationModel:
    def __init__(self, n_estimators=100, random_state=42):
        self.model = RandomForestRegressor(n_estimators=n_estimators, random_state=random_state)
    
    def train(self, data):
        X = data[['Product_Cost', 'Product_Price']]
        y = data['Units']
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(self.X_train, self.y_train)
    
    def evaluate(self):
        predictions = self.model.predict(self.X_test)
        mse = mean_squared_error(self.y_test, predictions)
        r2 = r2_score(self.y_test, predictions)
        return {"mse": mse, "r2": r2}
    
    def predict_units(self, cost, price):
        input_data = pd.DataFrame([[cost, price]], columns=['Product_Cost', 'Product_Price'])
        return self.model.predict(input_data)[0]
    
    def optimize_price(self, product_cost, price_range):
        profits = []
        for price in price_range:
            units_sold = self.predict_units(product_cost, price)
            profit = (price - product_cost) * units_sold
            profits.append(profit)
        optimal_price = price_range[np.argmax(profits)]
        return optimal_price, max(profits)
