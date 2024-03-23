from .base_energy_model import BaseEnergyModel

class ShortTermEnergyModel(BaseEnergyModel):
    """
    A model designed for short-term energy consumption forecasting.

    Args:
        df (pd.DataFrame): The DataFrame containing the data for model training and prediction.
    """
    def __init__(self, df):
        # Initialize the base class with specific parameters for short-term forecasting
        super().__init__(df,
                         column_names=['total_consumption', 'day_length', 'dayofweek'],
                         external_features=['day_length'],  
                         lags=[1, 2, 3, 4, 5, 6, 7, 30],
                         window_sizes=[2, 3, 4, 5, 6, 7, 30])