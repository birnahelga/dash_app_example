# coding: utf-8

# # Final Project
# 
# Create a Dashboard taking data from [Eurostat, GDP and main components (output, expenditure and income)](http://ec.europa.eu/eurostat/web/products-datasets/-/nama_10_gdp). 
# The dashboard will have two graphs: 
# 
# * The first one will be a scatterplot with two DropDown boxes for the different indicators. It will have also a slide for the different years in the data. 
# * The other graph will be a line chart with two DropDown boxes, one for the country and the other for selecting one of the indicators. (hint use Scatter object using mode = 'lines' [(more here)](https://plot.ly/python/line-charts/) 

# In[40]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash(__name__)
server = app.server
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

df1 = pd.read_csv('nama_10_gdp_1_Data.csv',na_values=':')

#remove European Union and Euro area
df = df1[~df1['GEO'].str.contains('Euro')]

#rename Germany, Kosovo and FYR Macedonia
df= df.replace({'Germany (until 1990 former territory of the FRG)': 'Germany',
                'Kosovo (under United Nations Security Council Resolution 1244/99)': 'Kosovo',
                'Former Yugoslav Republic of Macedonia, the': 'FYR Maceodonia'
               })

available_indicators = sorted(df['NA_ITEM'].unique())
available_geo=sorted(df['GEO'].unique())
available_unit=sorted(df['UNIT'].unique())
available_year=df['TIME'].unique()


app.layout = html.Div(style={'backgroundColor': '#F5E6F6'},children=[
    
    html.H1('Final Project Dash - Birna Helga', 
            style={
            'textAlign': 'center',
            'color': 'darkviolet'
        }),
    
    html.H4('Graph 1: Scatterplot', 
            style={
            'color': 'darkviolet'
        } ),

    
    #First graph
    html.Div([
        
        html.Div([
            dcc.Dropdown(
                id='xaxis-column1',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            ),
            dcc.RadioItems(
                id='xaxis-type1',
                options=[{'label': i, 'value': i} for i in available_unit],
                value='Current prices, million euro',
                labelStyle={'display': 'inline-block'}
            )
                    
        ],
        style={'width': '45%','padding':20, 'display': 'inline-block'}),
        
        html.Div([
            dcc.Dropdown(
                id='yaxis-column1',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Imports of goods'
            ),
            dcc.RadioItems(
                id='yaxis-type1',
                options=[{'label': i, 'value': i} for i in available_unit],
                value='Current prices, million euro',
                labelStyle={'display': 'inline-block'}
            )
        ],style={'width': '45%','padding':20,'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='indicator-graphic'),

    dcc.Slider(
        id='year--slider',
        min=df['TIME'].min(),
        max=df['TIME'].max(),
        value=df['TIME'].max(),
        step=None,
        marks={str(year): str(year) for year in df['TIME'].unique()}
    ),
    
    #Second graph
        
    html.H4('Graph 2: Line chart', 
            style={
            'color': 'hotpink'
        } ),
    
    html.Div([
        
        html.Div([
            dcc.Dropdown(
                id='xaxis-column2',
                options=[{'label': i, 'value': i} for i in available_geo],
                value='Spain'
            )
                    
        ],
        style={'width': '35%', 'padding':30, 'display': 'inline-block'}),
        
        html.Div([
            dcc.Dropdown(
                id='yaxis-column2',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            ),
            dcc.RadioItems(
                id='yaxis-type2',
                options=[{'label': i, 'value': i} for i in available_unit],
                value='Current prices, million euro',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '55%','padding':30, 'float': 'right', 'display': 'inline-block'})    
    ]),

    dcc.Graph(id='indicator-graphic2'),
])


@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-column1', 'value'),
     dash.dependencies.Input('yaxis-column1', 'value'),
     dash.dependencies.Input('xaxis-type1', 'value'),
     dash.dependencies.Input('yaxis-type1', 'value'),
     dash.dependencies.Input('year--slider', 'value')])
def update_graph(xaxis_column_name1, yaxis_column_name1,
                 xaxis_type1, yaxis_type1,
                 year_value1):
    dfx = df[(df['TIME'] == year_value1)&(df['UNIT'] == xaxis_type1)]
    dfy = df[(df['TIME'] == year_value1)&(df['UNIT'] == yaxis_type1)]
    
    return {
        'data': [go.Scatter(
            x=dfx[(dfx['NA_ITEM'] == xaxis_column_name1) & (dfx['GEO']==i)]['Value'],
            y=dfy[(dfy['NA_ITEM'] == yaxis_column_name1) & (dfy['GEO']==i)]['Value'],
            text=i, 
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }, name=i ) for i in available_geo
        ],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name1,
                'type': 'linear',
                'color':'darkviolet',
            },
            yaxis={
                'title': yaxis_column_name1,
                'type': 'linear',
                'color':'darkviolet'
            },
            margin={'l': 60, 'b': 60, 't': 10, 'r': 30},
            hovermode='closest',
            plot_bgcolor='#F5E6F6',
            paper_bgcolor= '#F5E6F6',
            font={'color': 'darkviolet'}
        )
    }

@app.callback(
    dash.dependencies.Output('indicator-graphic2', 'figure'),
    [dash.dependencies.Input('xaxis-column2', 'value'),
     dash.dependencies.Input('yaxis-column2', 'value'),
     dash.dependencies.Input('yaxis-type2', 'value')])
def update_graph(xaxis_column_name2, yaxis_column_name2,yaxis_type2):
    dfz=df[(df['GEO']==xaxis_column_name2)&(df['UNIT']==yaxis_type2)]
    
    return {
        'data': [go.Scatter(
            x=available_year,
            y=dfz[dfz['NA_ITEM'] == yaxis_column_name2]['Value'],
            text=available_year, 
            mode='lines',
            line={'width': 2.5, 'color': 'hotpink'}
        )],
        'layout': go.Layout(
            xaxis={
                'title': 'Year',
                'type': 'date',
                'linecolor':'hotpink',
                'color':'hotpink'
            },
            yaxis={
                'title': yaxis_column_name2,
                'type': 'linear',
                'linecolor':'hotpink',
                'color':'hotpink'
            },
            margin={'l': 60, 'b': 60, 't': 10, 'r': 30},
            hovermode='closest',
            plot_bgcolor='#F5E6F6',
            paper_bgcolor= '#F5E6F6',
        )
    }

if __name__ == '__main__':
    app.run_server()

