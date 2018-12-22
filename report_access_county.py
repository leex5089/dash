import os

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
from plotly import graph_objs as go
import json
import pandas as pd
import numpy as np
import plotly
import plotly.graph_objs as go
import numpy as np
import plotly 
import urllib

app = dash.Dash(__name__)
server = app.server

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

df_ranking = pd.read_csv(
"https://raw.githubusercontent.com/leex5089/dash/master/access_trend_county_rank.csv"
)


DF_GAPMINDER = pd.read_csv(
    'https://raw.githubusercontent.com/leex5089/dash/master/access_trend_county.csv'
)

df_string = pd.read_csv(
    'https://raw.githubusercontent.com/leex5089/dash/master/access_trend_county2.csv'
)

df = pd.read_csv(
    'https://raw.githubusercontent.com/leex5089/dash/master/access_trend_county2.csv'
)


df4= pd.read_csv(
    'https://raw.githubusercontent.com/leex5089/dash/master/access_trend_county.csv'
)
df4c=df4
 




YEARS=DF_GAPMINDER.year

available_indicators = df['varname'].unique()
county_indicators = DF_GAPMINDER['county'].unique()


 

def make_dash_table( df ):
    ''' Return a dash definitio of an HTML table for a Pandas dataframe '''
    table = []
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append( html.Td([ row[i] ]) )
        table.append( html.Tr( html_row ) )
    return table


def print_button():
    printButton = html.A(['Print PDF'],className="button no-print print",style={'position': "absolute", 'top': '-40', 'right': '0'})
    return printButton

# includes page/full view
def get_logo():
    logo = html.Div([

        html.Div([
            html.Img(src='https://imgur.com/NfaqV5u', height='40', width='160')
        ], className="ten columns padded"),

        html.Div([
            dcc.Link('Full View   ', href='/full-view')
        ], className="two columns page-view no-print")

    ], className="row gs-header")
    return logo


#START
    
app.layout = html.Div([
    html.Div([# page 1
    html.A(['Print PDF'],
               className="button no-print",
               style=dict(position="absolute", top=-40, right=0)),
    html.Div([# subpage 1
    html.Div([
    html.Div([
    html.H3(' Minnesota Child Care Access Report'),
                        html.Div(' Choose a year of interest from the slide menu below',
                                 style={'color': 'rgb(204,255,255)', 'fontSize': 14}),

                        html.Div([
                         html.Div(dcc.Slider(
                            id='crossfilter-year--slider',
                            min=df['year'].min(),
                            max=df['year'].max(),
                            value=df['year'].max(),
                            step=None,
                            marks={str(year): str(year) for year in df['year'].unique()}
                        ), style={'width': '60%', 'padding': '20px 20px 20px 20px', 'textAlign': 'center'},
                            className="row"),

                        html.Div(' Choose a county of interest from the drop-down menu below',
                             style={'color': 'rgb(204,255,255)', 'fontSize': 14}),
                            html.Div(dcc.Dropdown(
                            id='county-dropdown',
                            options=[{'label': i, 'value': i} for i in county_indicators],
                            multi=False,
                            value='Hennepin'
                            ),
                            style={'width': '40%', 'padding': '20px 20px 20px 20px', 'textAlign': 'left', 'fontSize': 14,'color': 'black'}),
                     ], className="seven columns"),      
                     ]), 


        html.Div([
                        html.Div(id='heatmap-title3',style={'color': '#ffffff', 'fontSize': 20}),
                                                    
                        html.Div(id='heatmap-title2',style={'color': '#ffffff', 'fontSize': 20}),
            ], className="five columns gs-header gs-accent-header padded", style=dict(float='right')),
          ], className="row gs-header gs-text-header"),


        html.Div([
                html.H6('Access Information',style = {'width': '100%', 'display': 'inline-block', 'padding': '0 20','marginBottom': 10, 'marginTop': 10,'textAlign': 'center'}, className="gs-header gs-text-header padded"),

            html.P('This report summarizes county-level child care access measures in Minnesota.', 
                        style = {'width': '100%', 'display': 'inline-block', 'padding': '0 0','marginBottom': 10, 'marginTop': 10,'textAlign': 'center', 'fontSize': 15},
                        className='blue-text'),

  
        ], className="row"),

            # Row 2
            html.Div([
                html.Div([
                    html.H6('Averages', className="gs-header gs-text-header padded"), html.Table(id='my-table' , style = {'fontSize': 12}),
                ], style = {'width': '50%', 'display': 'inline-block', 'padding': '0 20','marginBottom': 10, 'marginTop': 10,'textAlign': 'center'}, className=" six columns"),

                html.Div([
                    html.H6('Ranking', className="gs-header gs-text-header padded"),
                    html.Table(id='my-table_rank' , style = {'fontSize': 12} ),
                ], style={'width': '50%', 'display': 'inline-block', 'padding': '0 20','marginBottom': 10, 'marginTop': 10,'textAlign': 'center'}, className=" six columns" ),
                ], className="row "),
                        html.Div([
                            html.H6('Time Trend', className="gs-header gs-text-header padded"),
                                                    ], style={'width': '100%', 'display': 'inline-block', 'padding': '0 20','marginBottom': 10, 'marginTop': 10,'textAlign': 'center'},
                            className=" row"),

                html.Div([
                    html.Div([
                        dcc.Graph(id='graphs-new3',
                                  config={
                            'displayModeBar': False
                        }),
                    ],style={'display': 'inline-block'}, className="six columns"),
                    html.Div([
                        dcc.Graph(id='graphs-new4',config={
                            'displayModeBar': False
                        }),
                    ],style={'display': 'inline-block'}, className="six columns"),
                ], className="row "),

        html.Div([

            html.Div([
                dcc.Graph(id='graphs-new5',
                          config={
                              'displayModeBar': False
                          }),
            ], style={'display': 'inline-block'}, className="six columns"),
        
        html.Div([
                dcc.Graph(id='graphs-new6', config={
                    'displayModeBar': False
                }),
            ], style={'display': 'inline-block'}, className="six columns"),
        ], className="row "),
             ], className = "subpage" )
            ], className="page"),


    html.Div([ # page 2
    html.Div([# subpage 2
     html.Div([
            html.H6('Data Table',style = {'width': '100%', 'display': 'inline-block', 'padding': '0 20','marginBottom': 10, 'marginTop': 10,'textAlign': 'center'}, className="gs-header gs-text-header padded"),

            html.P('Use filter and sort function to view the data.', className='blue-text'),


        ], className="row"),

            # Row 2
 
        
        html.Div([
        dt.DataTable(
            rows=df4c.to_dict('records'),
            # optional - sets the order of columns
            columns=sorted(df4c.columns),
            row_selectable=True,
            filterable=True,
            sortable=True,
            max_rows_in_viewport=10,
            min_height=300,
            selected_row_indices=[],
            id='datatable-gapminder'
        )
        ], style={'width': '100%', 'height': '480'}),

        html.Div(id='selected-indexes'),
        html.A(
            'Check the boxes in the table and download the data.',
            id='download-link',
            download='rawdata.csv',
            href='',
            target="_blank"
        ),
        dcc.Graph(
            id='graph-gapminder',config={
                'displayModeBar': False
            }, style={'width': '100%', 'height': '350'}
        ),

], className = "subpage" ),
                        ], className="page")
        ])


external_css = ["https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",
                "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "//fonts.googleapis.com/css?family=Raleway:400,300,600",
                "https://codepen.io/plotly/pen/KmyPZr.css",
                "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"]

for css in external_css:
    app.css.append_css({"external_url": css})

external_js = ["https://code.jquery.com/jquery-3.2.1.min.js",
               "https://codepen.io/plotly/pen/KmyPZr.js"]

for js in external_js:
    app.scripts.append_script({"external_url": js})


    def filter_data(selected_row_indices):
        dff = df4.iloc[selected_row_indices]
        return dff




@app.callback(dash.dependencies.Output('heatmap-title3', 'children'),
              [dash.dependencies.Input('county-dropdown', 'value')])
def display_value(value):
    return '{}'.format(value) + ' County'

@app.callback(dash.dependencies.Output('heatmap-title2', 'children'),
              [dash.dependencies.Input('crossfilter-year--slider', 'value')])
def display_value(value):
    return 'Year {}'.format(value)




@app.callback(
        dash.dependencies.Output('graph-gapminder', 'figure'),
        [dash.dependencies.Input('datatable-gapminder', 'rows'),
         dash.dependencies.Input('datatable-gapminder', 'selected_row_indices'),
         dash.dependencies.Input('crossfilter-year--slider', 'value')
         ])
def update_figure(rows, selected_row_indices, year_value):
        dff = pd.DataFrame(rows)
        dff2 = dff[dff['year'] == year_value]
        fig = plotly.tools.make_subplots(
            rows=3, cols=1,
            subplot_titles=('Supply_Any', 'Supply_HR', 'Cost_Any'),
            shared_xaxes=True)
        marker = {'color': ['rgb(8,48,107)'] * len(dff2)}
        for i in (selected_row_indices or []):
            marker['color'][i] = 'rgba(222,45,38,0.8)'
        fig.append_trace({
            'x': dff2['county'],
            'y': dff2['Supply_Any'],
            'type': 'bar',
            'marker': marker
        }, 1, 1)
        fig.append_trace({
            'x': dff2['county'],
            'y': dff2['Supply_HR'],
            'type': 'bar',
            'marker': marker
        }, 2, 1)
        fig.append_trace({
            'x': dff2['county'],
            'y': dff2['Cost_Any'],
            'type': 'bar',
            'marker': marker
            }, 3, 1)
        fig['layout']['showlegend'] = False
        fig['layout']['height'] = 290
        fig['layout']['margin'] = {
            'l': 40,
            'r': 20,
            't': 30,
            'b': 100
        }
        fig['layout']['font'] ={"family": "Raleway","size": 8}
        fig['layout']['titlefont'] ={"size": 8}


        return fig



@app.callback(
        dash.dependencies.Output('download-link', 'href'),
        [dash.dependencies.Input('datatable-gapminder', 'selected_row_indices')])
def update_download_link(selected_row_indices):
        dff = filter_data(selected_row_indices)
        csv_string = dff.to_csv(index=False, encoding='utf-8')
        csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
        return csv_string

@app.callback(dash.dependencies.Output('my-table', 'children'),
                  [dash.dependencies.Input('county-dropdown', 'value'),
                   dash.dependencies.Input('crossfilter-year--slider', 'value')
                   ])
def table_update(selected_county,selected_year):
        df1 = df_string[df_string['county'] == selected_county]
        df2 = df1[df1['year'] == selected_year]
        return make_dash_table(df2)

@app.callback(dash.dependencies.Output('my-table_rank', 'children'),
                  [dash.dependencies.Input('county-dropdown', 'value'),
                   dash.dependencies.Input('crossfilter-year--slider', 'value')
                   ])
def table_update(selected_county,selected_year):
        df1_rank = df_ranking[df_ranking['county'] == selected_county]
        df2_rank = df1_rank[df1_rank['year'] == selected_year]
        return make_dash_table(df2_rank)

@app.callback(
        dash.dependencies.Output('graphs-new3', 'figure'),
        [dash.dependencies.Input('county-dropdown', 'value')])
def update_figure(selected_county):
        filtered_df = DF_GAPMINDER[DF_GAPMINDER['county'] == selected_county]
        return {
            'data': [go.Scatter(
                x=filtered_df['year'],
                y=filtered_df['Supply_Any'],
                text=filtered_df['county'],
                mode='lines+markers',
                marker={
                    'size': 5,
                    'opacity': 0.5,
                    'color': 'rgb(8,48,107)',
                    'line': {'width': 0.5, 'color': 'red'}
                }
            )],
            'layout': go.Layout(
                autosize=False,
                height=140,
                width=350,
                xaxis={'title': 'year'},
                yaxis={'title': 'Adj Supply [Any]', 'range': [0,2]},
                margin={'l': 40, 'b': 40, 't': 40, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest',
                font={
                    "family": "Raleway",
                    "size": 10
                }
            )
        }

@app.callback(
        dash.dependencies.Output('graphs-new4', 'figure'),
        [dash.dependencies.Input('county-dropdown', 'value')])
def update_figure(selected_county):
        filtered_df = DF_GAPMINDER[DF_GAPMINDER['county'] == selected_county]

        return {
            'data': [go.Scatter(
                x=filtered_df['year'],
                y=filtered_df['Supply_CCC'],
                text=filtered_df['county'],
                mode='lines+markers',
                marker={
                    'size': 5,
                    'opacity': 0.5,
                    'color': 'rgb(8,48,107)',
                    'line': {'width': 0.5, 'color': 'red'}
                }
            )],
            'layout': go.Layout(
                autosize=False,
                height=140,
                width=350,
                xaxis={'title': 'year'},
                yaxis={'title': 'Adj Supply [CCC]', 'range': [0,2]},
                margin={'l': 40, 'b': 40, 't': 40, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest',
            font={
                     "family": "Raleway",
                     "size": 10
                 }
            )
        }


@app.callback(
        dash.dependencies.Output('graphs-new5', 'figure'),
        [dash.dependencies.Input('county-dropdown', 'value')])
def update_figure(selected_county):
        filtered_df = DF_GAPMINDER[DF_GAPMINDER['county'] == selected_county]
        return {
            'data': [go.Scatter(
                x=filtered_df['year'],
                y=filtered_df['Cost_Any'],
                text=filtered_df['county'],
                mode='lines+markers',
                marker={
                    'size': 5,
                    'opacity': 0.5,
                    'color': 'rgb(8,48,107)',
                    'line': {'width': 0.5, 'color': 'red'}
                }
            )],
            'layout': go.Layout(
                autosize=False,
                height=140,
                width=350,
                xaxis={'title': 'year'},
                yaxis={'title': 'Total Cost [Any]'},
                margin={'l': 40, 'b': 40, 't': 40, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest',
                font={
                    "family": "Raleway",
                    "size": 10
                }
            )
        }



@app.callback(
        dash.dependencies.Output('graphs-new6', 'figure'),
        [dash.dependencies.Input('county-dropdown', 'value')])
def update_figure(selected_county):
        filtered_df = DF_GAPMINDER[DF_GAPMINDER['county'] == selected_county]

        return {
            'data': [go.Scatter(
                x=filtered_df['year'],
                y=filtered_df['Cost_CCC'],
                text=filtered_df['county'],
                mode='lines+markers',
                marker={
                    'size': 5,
                    'opacity': 0.5,
                    'color': 'rgb(8,48,107)',
                    'line': {'width': 0.5, 'color': 'red'}
                }
            )],
            'layout': go.Layout(
                autosize=False,
                height=140,
                width=350,
                xaxis={'title': 'year'},
                yaxis={'title': 'Total Cost [CCC]' },
                margin={'l': 40, 'b': 40, 't': 40, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest',
            font={
                     "family": "Raleway",
                     "size": 10
                 }
            )
        }
@app.callback(Output('datatable-gapminder', 'rows'),
                  [Input('crossfilter-year--slider', 'value'),
                   ])
def update_rows2( selected_year):
        df4c = df4[df4['year'] == selected_year]
        return df4c.to_dict('records')









if __name__ == '__main__':
    app.run_server(debug=True)


