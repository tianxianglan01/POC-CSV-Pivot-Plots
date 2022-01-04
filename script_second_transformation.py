import pandas as pd
import plotly.express as px

problem_1_csv = ''
problem_2_3_csv = 'raw_and_cleaned_data/Output Csvs Script Tests/severe_events.csv'

colors = {'Snow': 'white', 'Fog': 'gray', 'Storm': 'red', 'Rain': 'green', 'Cold': 'blue', 'Precipitation': 'black', 'Hail': 'yellow'}

def prob2_graph():
    severe_df = pd.read_csv(problem_2_3_csv)
    most_events_state = severe_df.groupby('State').agg('sum').sort_values(by = ['Month'], ascending = False).head(10).index.values.tolist()
    severe_df = severe_df[severe_df['State'].isin(most_events_state)]
    severe_df = severe_df[['State', 'Month', 'Type']]
    severe_df = severe_df.groupby(['State', 'Type']).sum().reset_index().rename(columns={'Month': 'Severe Count'})
    fig = px.histogram(severe_df, title = 'Top Ten Severe Event by State', x = 'State', color = 'Type', y = 'Severe Count', color_discrete_map = colors)
    # fig.show()

    fig.write_image("Output_Graphs/top_ten_severe_event_states.jpeg")

def prob3_graph():
    severe_df2 = pd.read_csv(problem_2_3_csv)
    severe_df2 = severe_df2[['State', 'Month', 'Type']]
    months = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: "Apr", 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}

    grouped_df2 = severe_df2.groupby(['State', 'Month', 'Type']).sum()
    grouped_df2.reset_index(inplace = True)

    severe_df2 = severe_df2.replace({'Month': months})
    severe_df2['Count'] = 1

    grouped_df2 = severe_df2.groupby(['State', 'Month', 'Type']).sum()
    grouped_df2.reset_index(inplace = True)

    states = severe_df2['State'].unique().tolist()

    for i in states:
        df = df_ex = severe_df2.loc[severe_df2['State'] == i]
        fig = px.histogram(grouped_df2, title = "{state}'s Number of Severe Events by Month".format(state = i), x = 'Month', y = 'Count', color = 'Type', color_discrete_map = colors)
        fig.write_image("Output_Graphs/2nd Trans Prob 3/{state}.jpeg".format(state = i))




if __name__ == "__main__":
    prob3_graph()
   