import argparse
import os
import pandas as pd
from dotenv import load_dotenv
from models.short_term_energy_model import ShortTermEnergyModel
from models.long_term_energy_model import LongTermEnergyModel

# Load environment variables
load_dotenv()

def main(date, model_choice):
    # Load Processed Data
    data_path = os.getenv('PROCESSED_DATA_PATH')
    full_path = data_path + '/weather_and_consumption.csv'
    weather_and_consumption_df = pd.read_csv(full_path, index_col=0, parse_dates=True)

    # Model Selection
    if model_choice == 'short':
        model = ShortTermEnergyModel(weather_and_consumption_df)
        prediction = model.predict_for_date(date)
        print(f"Short-term prediction for {date}: {prediction}")
    elif model_choice == 'long':
        model = LongTermEnergyModel(weather_and_consumption_df)
        prediction = model.predict_for_date(date)
        print(f"Long-term prediction for {date}: {prediction}")
    else:
        print("Invalid model choice. Please choose 'short' for short-term or 'long' for long-term.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Energy Consumption Forecasting')
    parser.add_argument('-d', '--date', type=str, required=True, help='Date for prediction in YYYY-MM-DD format')
    parser.add_argument('-m', '--model', type=str, required=True, choices=['short', 'long'], help="Model choice: 'short' for short-term, 'long' for long-term")

    args = parser.parse_args()

    main(args.date, args.model)