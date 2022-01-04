import pandas as pd
import numpy as np

weather_2020_path = 'raw_and_cleaned_data/3 Partitions/weather_2020.csv'

def data_analysis(): 
    # data_analysis 1
    print('hello')
    selected_df = pd.read_csv(weather_2020_path)
    selected_df['Lat Decile'] = pd.qcut(selected_df['LocationLat'], 10)
    selected_df['Lat Decile Rank'] = pd.qcut(selected_df['LocationLat'], 10, labels = False)
    selected_df['Month'] = pd.DatetimeIndex(selected_df['StartTime(UTC)']).month
    selected_columns = selected_df[['Month', 'Lat Decile Rank', 'Lat Decile', 'Type']]
    analysis_1 = selected_columns.pivot_table(
                columns = ['Type'],
                           index = ['Month', 'Lat Decile Rank', 'Lat Decile'],
                           aggfunc = len)
    analysis_1 = analysis_1.reset_index()
    analysis_1.to_csv('raw_and_cleaned_data/Output Csvs Script Tests/types_by_latitude_by_month.csv', index = False)

    # data_analysis 2
    a_2_columns = selected_df[['Type', 'Month', 'State', 'Severity']]
    severe_events = a_2_columns[a_2_columns['Severity'] == 'Severe']
    severe_events.to_csv('raw_and_cleaned_data/Output Csvs Script Tests/severe_events.csv', index = False)


if __name__ == '__main__':
    data_analysis()