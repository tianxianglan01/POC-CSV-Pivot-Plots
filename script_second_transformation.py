import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

problem_1_csv = 'raw_and_cleaned_data/Output Csvs/types_by_latitude_by_month.csv'
problem_2_3_csv = 'raw_and_cleaned_data/Output Csvs Script Tests/severe_events.csv'

colors = {'Cold': 'lightblue', 'Fog': 'gray', 'Storm': 
              'red', 'Rain': 'lightgreen', 'Hail': 'yellow', 
              'Precipitation': 'black', 'Snow': 'white'}

weather_types = ['Cold', 'Fog', 'Storm', 'Rain', 'Hail', 'Precipitation', 'Snow']


def color_matcher(str_col):
    first_word_value = str_col.split()[0][:-1]
    if first_word_value in weather_types:
        return colors[first_word_value]

def prob1_graph():
    types_lat_month_df = pd.read_csv(problem_1_csv, index_col = [0])
    types_lat_month_df.fillna(value = 0, inplace = True)

    types_lat_month_df = types_lat_month_df[['Month', 'Lat Decile Rank', 'Lat Decile', 'Cold', 'Fog', 'Hail', 'Precipitation', 'Rain', 'Snow']]
    months = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: "Apr", 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}

    types_lat_month_df = types_lat_month_df.replace({'Month': months})

    types_lat_month_df[['Cold','Fog', 'Hail', 'Precipitation', 'Rain', 'Snow']] = types_lat_month_df[['Cold','Fog', 'Hail', 'Precipitation', 'Rain', 'Snow']].astype(int)

    types_lat_month_df['Most Events Type'] = types_lat_month_df[['Cold', 'Fog', 'Hail', 'Precipitation', 'Rain', 'Snow']].idxmax(axis=1)

    types_lat_month_df['Most Events Count'] = types_lat_month_df[['Cold', 'Fog', 'Hail', 'Precipitation', 'Rain', 'Snow']].max(axis = 1)

    types_lat_month_df['Most Events and Type'] = types_lat_month_df['Most Events Type'] + ', ' + types_lat_month_df['Most Events Count'].astype(str)
    
    selected_df = types_lat_month_df[['Month', 'Lat Decile Rank', 'Most Events Count', 'Most Events Type', 'Most Events and Type']]

    pivot_df = pd.pivot_table(selected_df, columns = ['Month'], index = ['Lat Decile Rank'], values = ['Most Events and Type'], aggfunc=lambda x: ' '.join(x))

    ordered_columns = [('Most Events and Type', 'Jan'), ('Most Events and Type', 'Feb'), ('Most Events and Type', 'Mar'), 
                    ('Most Events and Type', 'Apr'), ('Most Events and Type', 'May'), ('Most Events and Type', 'Jun'),
                    ('Most Events and Type', 'Jul'), ('Most Events and Type', 'Aug'), ('Most Events and Type', 'Sep'),
                    ('Most Events and Type', 'Oct'), ('Most Events and Type', 'Nov'), ('Most Events and Type', 'Dec')]

    pivot_df = pivot_df[ordered_columns]
    pivot_df.columns = pivot_df.columns.map(': '.join)
    pivot_df = pivot_df.reset_index()

    

    trace = dict(type = 'table', 
            header = dict(values=list(pivot_df.columns), align = 'left'),
            cells = dict(values = [
                        pivot_df['Lat Decile Rank'], pivot_df['Most Events and Type: Jan'], pivot_df['Most Events and Type: Feb'], pivot_df['Most Events and Type: Mar'], 
                        pivot_df['Most Events and Type: Apr'], pivot_df['Most Events and Type: May'], pivot_df['Most Events and Type: Jun'], pivot_df['Most Events and Type: Jul'], 
                        pivot_df['Most Events and Type: Aug'], pivot_df['Most Events and Type: Sep'], pivot_df['Most Events and Type: Oct'],pivot_df['Most Events and Type: Nov'], 
                        pivot_df['Most Events and Type: Dec']],
                        align = 'center',
                        fill = dict(color = ['rgb(245, 245, 245)', [color_matcher(val) for val in pivot_df['Most Events and Type: Jan']],
                
                                    [color_matcher(val) for val in pivot_df['Most Events and Type: Feb']],
                                    [color_matcher(val) for val in pivot_df['Most Events and Type: Mar']],
                                    [color_matcher(val) for val in pivot_df['Most Events and Type: Apr']],
                                    [color_matcher(val) for val in pivot_df['Most Events and Type: May']],
                                    [color_matcher(val) for val in pivot_df['Most Events and Type: Jun']],
                                    [color_matcher(val) for val in pivot_df['Most Events and Type: Jul']],
                                    [color_matcher(val) for val in pivot_df['Most Events and Type: Aug']],
                                    [color_matcher(val) for val in pivot_df['Most Events and Type: Sep']],
                                    [color_matcher(val) for val in pivot_df['Most Events and Type: Oct']],
                                    [color_matcher(val) for val in pivot_df['Most Events and Type: Nov']],
                                    [color_matcher(val) for val in pivot_df['Most Events and Type: Dec']]
                                    ]
                                               
                                   ))
            
            )
            
    trace['cells']['fill']
    fig = go.Figure(data = [go.Table(
        header = dict(values=list(pivot_df.columns),
            align='left'),
        cells = dict(values = [pivot_df['Lat Decile Rank'], pivot_df['Most Events and Type: Jan'], 
                        pivot_df['Most Events and Type: Feb'], pivot_df['Most Events and Type: Mar'], pivot_df['Most Events and Type: Apr'],
                        pivot_df['Most Events and Type: May'], pivot_df['Most Events and Type: Jun'], pivot_df['Most Events and Type: Jul'], 
                        pivot_df['Most Events and Type: Aug'], pivot_df['Most Events and Type: Sep'], pivot_df['Most Events and Type: Oct'],
                        pivot_df['Most Events and Type: Nov'], pivot_df['Most Events and Type: Dec']],
                        align = 'center')),
                                       
            ])

    fig = fig.add_traces(data = [trace])
    fig.write_image("output_Graphs/most_common_events_by_latitude_by_month.jpeg", width = 1200, height = 800)




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
    prob1_graph()
    prob2_graph()
    prob3_graph()
   