from .base_energy_model import BaseEnergyModel

class LongTermEnergyModel(BaseEnergyModel):
    """
    A model designed for long-term energy consumption forecasting.

    Args:
        df (pd.DataFrame): The DataFrame containing the data for model training and prediction.
    """
    def __init__(self, df):
        # Initialize the base class with specific parameters for long-term forecasting
        super().__init__(df,
                         column_names=['total_consumption', 'day_length'],
                         external_features=['feelslike', 'temp', 'day_length', 'tempmax'],
                         lags=[30, 40, 365], 
                         window_sizes=[])  # No moving averages are used, to prevent data leakage