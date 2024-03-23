# Supress warnings
import warnings ; warnings.filterwarnings('ignore')

# Data manipulation
import numpy as np
import pandas as pd

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns ; color_pal = sns.color_palette("husl", 9) ; plt.style.use('fivethirtyeight')

# Machine Learning
from sklearn.ensemble import RandomForestRegressor


class BaseEnergyModel:
    """
    A base model for predicting energy consumption using RandomForestRegressor.

    Attributes:
        df (pd.DataFrame): The DataFrame containing the data for model training.
        column_names (list): List of column names to be used as predictors.
        external_features (list): List of external features to be used in the model.
        lags (list): List of integers representing the lag values for creating lag features.
        window_sizes (list): List of integers representing window sizes for creating rolling mean features.
        model (RandomForestRegressor): The Random Forest model for prediction.
        created_features (list): List of created feature names after feature engineering.
    """
    def __init__(self, df, column_names, external_features, lags, window_sizes, n_estimators=600, max_depth=3):
        """
        Initializes the model with data and training parameters.

        Args:
            df (pd.DataFrame): The dataset to be used for training the model.
            column_names (list): Names of the columns to predict.
            external_features (list): Names of external predictor variables.
            lags (list): Lag periods for generating lagged features.
            window_sizes (list): Window sizes for generating rolling features.
            n_estimators (int, optional): The number of trees in the forest. Defaults to 600.
            max_depth (int, optional): The maximum depth of the tree. Defaults to 3.
        """
        self.df = df
        self.column_names = column_names
        self.external_features = external_features
        self.lags = lags
        self.window_sizes = window_sizes
        self.model = RandomForestRegressor(n_estimators=n_estimators, max_depth=max_depth)
        self.created_features = []
        self._create_features()
        self._train()

    def plot_feature_importance(self, top_n=10):
        """
        Plots the top N feature importances of the trained RandomForestRegressor model using Seaborn.
        Args:
        - top_n (int): Number of top features to plot.
        """
        # Ensure the model has been trained before plotting
        if not hasattr(self, 'model') or not hasattr(self.model, 'feature_importances_'):
            print("Model must be trained before plotting feature importances.")
            return
        
        features = self.created_features + self.external_features
        importances = self.model.feature_importances_
        
        # Create DataFrame for feature importances
        feature_data = pd.DataFrame({
            'Feature': features,
            'Importance': importances
        }).sort_values(by='Importance', ascending=False).head(top_n)
        
        # Plotting
        plt.figure(figsize=(20, 5))
        sns.barplot(data=feature_data, x='Importance', y='Feature', palette='viridis')
        
        # Adding titles and labels
        model_type = "Short-Term" if isinstance(self, ShortTermEnergyModel) else "Long-Term"
        plt.title(f'{model_type} Model: Top {top_n} Features', fontsize=16)
        plt.xlabel('Feature Importance', fontsize=12)
        plt.ylabel('Feature', fontsize=12)
        
        # Adjust layout and display the plot
        plt.tight_layout()
        plt.show()

    def _create_features(self):
        """
        Performs feature engineering to create lagged and rolling mean features.
        """
        self.df['dayofweek'] = self.df.index.dayofweek
        self.created_features.append('dayofweek')

        for column_name in self.column_names:
            for lag in self.lags:
                feature_name = f"{column_name}_lag_{lag}"
                self.df[feature_name] = self.df[column_name].shift(lag)
                self.created_features.append(feature_name)

            for window in self.window_sizes:
                feature_name = f"{column_name}_rolling_mean_{window}"
                self.df[feature_name] = self.df[column_name].shift(1).rolling(window=window).mean()
                self.created_features.append(feature_name)

    def _train(self):
        """
        Trains the RandomForestRegressor model on the engineered features.
        """
        features = self.created_features + self.external_features
        X_train = self.df[features].dropna()
        y_train = self.df[self.column_names[0]].loc[X_train.index]
        self.used_features = list(X_train.columns)
        self.model.fit(X_train, y_train)

    def predict_for_date(self, date):
        """
        Predicts total consumption for a specified date using the trained model.

        Args:
            date (str): The date for which to predict consumption, in 'YYYY-MM-DD' format.

        Returns:
            float: The predicted consumption value, or None if prediction cannot be made.
        """
        date = pd.to_datetime(date)

        if date not in self.df.index:
            print(f"No direct data available for {date}, prediction requires feature presence.")
            return None

        features_order = self.created_features + self.external_features
        X_test = self.df.loc[[date], features_order]

        if not X_test.empty:
            prediction = self.model.predict(X_test)
            return prediction[0]
        else:
            print("Features not available for prediction.")
            return None