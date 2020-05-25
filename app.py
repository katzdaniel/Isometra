import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State
import dash_table
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd

import base64, io
from datetime import date


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

sample_df = pd.read_csv('data/sample_data.csv')

DASHBOARD_NAME = "Isometra"

def date_obj_from_iso_str(iso_str):

    date_arr = [int(i) for i in iso_str.split('-')]
    return date(date_arr[0], date_arr[1], date_arr[2])


def gen_monthly_revenue_bar_chart(full_df):

    g = px.bar(
        data_frame=full_df,
        x='Date',
        y='Monthly_Revenue',
    )

    g.update_layout(
        yaxis_title="Monthly Revenue",
        title = "Monthly Revenue Over Time"
    )
    
    return g

def analyze_metric(full_df, keyword, print_word):
    values = full_df[keyword].tolist()
    #growth_b = (values[13]/values[1] -1) * 100.0
    #growth_d = (values[17]/values[13] -1) * 100.0
   # growth_a = (values[-1]/values[17] -1) * 100.0

    before_data = abs((values[13]/values[1]-1)*100.0)
    during_data = abs((values[16]/values[13]-1)*100.0)
    after_data = abs((values[-1]/values[16]-1)*100.0)

    # return f"Before COVID, your {print_word} grew by {round(growth_b,2)}%, during COVID, your {print_word} grew by {round(growth_d,2)}%, and after COVID, your {print_word} has grown by {round(growth_a,2)}%."
    return f"Before COVID, your {print_word} {'shrank' if values[13]-values[1] < 0 else 'grew'} by {round(before_data,2)}%, during COVID, your {print_word} {'shrank' if values[17]-values[13] < 0 else 'grew'} by {round(during_data,2)}%, and since COVID, your {print_word} {'shrunk' if values[-1]-values[17] < 0 else 'grew'} by {round(after_data,2)}%"
     
    #df = full_df[keyword]

#    before_data = ((df['2020-03-01']-df['2010-01-01'])**(1/15)-1)*100
#     during_data = ((df['2020-06-01']-df['2010-03-01'])**(1/4)-1)*100
#     after_data = ((df['2020-07-01']-df['2010-06-01'])**(1/2)-1)*100


   # fig = go.Figure(data=[go.Table(header=dict(values=['Before', 'During','After']),
      #  cells=dict(values=[[before_data+'%'], [during_data+'%'],[after_data+'%']]))
     #   ])
  #  return fig
     
    
    #average growth = (endamount/startingamount - 1) * 100
    
    #percent growth
    # iterates through each item in "Net Income"
    # calculates how much more this was then before (percent-wise)
    # counter that keeps track of the percent growth and then finds the average
    # calculates the average growth in income before, during and after covid
    
def gen_monthly_expenditures_bar_chart(full_df):
    g = px.bar(
        data_frame=full_df,
        x='Date',
        y='Monthly_Expenditures'
    )
    
    g.update_layout(
        yaxis_title= "Monthly Expenditures",
        titles = "Monthly Expenditures Over Time"
    )
    return g

def gen_net_income_line_chart(full_df): 

    df_melt = full_df.melt(id_vars='Date', value_vars=['Net_Income', 'Monthly_Revenue','Monthly_Expenditures'])
    
    g = px.line(
        data_frame=df_melt,
        x='Date',
        y='value',
        color='variable',
        #'Monthly_Expenditures','Monthly_Revenue']
        labels={'value': 'Dollars'}
    )
    
    g.update_layout(
        yaxis_title="Input-Output Sales",
        title = "Net Income over Time"
    )
    
    return g

def gen_operating_margin_bar_chart(full_df):
    g = px.bar(
        data_frame=full_df,
        x='Date',
        y='Operating_Margin',
       # yaxis_title="Operating Margin"
    )
    g.update_layout(
        yaxis_title="Operating Margin",
        title = "Operating Margin Over Time"
    )
    return g

def gen_revenue_per_hour_line_chart(full_df):
    g = px.line(
        data_frame=full_df,
        x='Date',
        y='Revenue_Per_Hour',
    )
    g.update_layout(
        yaxis_title="Average Revenue Per Hour",
        title = "Revenue Per Hour Over Time"
    )
    return g
    

def gen_assets_capital_bar_chart(full_df):
    df_melt = full_df.melt(id_vars='Date', value_vars = ['Assets','Capital'])

    g = px.bar(
        data_frame=df_melt,
        x='Date',
        y='value',
        color='variable',
        barmode='group'
    )
    g.update_layout(
        yaxis_title="Assets and Capital",
        title = "Assets and Capital vs. Time"
    )
    return g
    
def gen_expenses_proportion_pie_chart(full_df, month ='2020-01-01'):

    labels = ['Employees_Paid','Rent_Paid','Other_Expenses','Loans_Paid', 'Taxes_Paid', 'Operations_Costs']

    month_row_df = full_df[full_df['Date'] == month]
    month_row_dict = month_row_df.to_dict() 
    values = [list(month_row_dict[i].values())[0] for i in labels]

    g = go.Figure(data=[go.Pie(labels=labels, values=values)])
    g.update_layout(
        title = "Percentage of Expenses by Category"
    )
    return g
    
def gen_revenue_proportion_pie_chart(full_df, month='2020-01-01'):

    labels = ['Services_Income', 'Investors', 'Loans_Taken', 'Other_Income', 'Grants']

    month_row_df = full_df[full_df['Date'] == month]
    month_row_dict = month_row_df.to_dict() 
    values = [list(month_row_dict[i].values())[0] for i in labels]

    g = go.Figure(data=[go.Pie(labels=labels, values=values)])
    g.update_layout(
        title = "Percentage of Revenue by Category",
    )
    return g

#HTML layout
app.layout = html.Div([
    
    html.Div([

        # first row div
        html.Div([

            # html.P('', className='one columns'),

            html.H1(DASHBOARD_NAME, className='three columns', id='header-title'),

            html.Div(
                html.P('My Cupcake Shop', id='header-desc-text'),
                className='six columns', id='header-desc-text-div'),

            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')], 
                    id='upload-data-text'),
                multiple=False,
                style={
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center'
                },
                className='three columns')

        ], className='row'),

        html.Div([
            
            html.P('A post-COVID business analytics dashboard', className='eight columns'),

            dcc.Dropdown(
                id='pie-chart-selector-dropdown',
                options=[{'label': date_obj_from_iso_str(i).strftime('%b %Y'), 'value': i} for i in sample_df['Date'].unique()],
                className='four columns',
                value='2020-01-01'),
        ], className='row'),

        html.Div([

        
            dcc.Graph(figure=gen_net_income_line_chart(sample_df), className='four columns', id='net-income-line-chart'),
            dcc.Graph(figure=gen_monthly_revenue_bar_chart(sample_df), className='four columns', id='monthly-revenue-bar-chart'),
            dcc.Graph(figure=gen_expenses_proportion_pie_chart(sample_df), className='four columns', id='expenses-proportion-pie-chart'),

        ], className='row'),

        html.Div([
            dcc.Graph(figure=gen_revenue_per_hour_line_chart(sample_df), className='four columns', id='revenue-per-hour-line-chart'),
            dcc.Graph(figure=gen_assets_capital_bar_chart(sample_df), className='four columns', id='assets-capital-bar-chart'),
            dcc.Graph(figure=gen_revenue_proportion_pie_chart(sample_df), className='four columns', id='revenue-proportion-pie-chart'),
            
        ], className='row'),

        
        html.Div([


            html.H5('Analysis', className='twelve columns', id='analysis-header')
        ], className='row'),
        
        #dropdown to select metric (column) to analyze
        html.Div([
            html.P("", className ='two columns'),

            dcc.Dropdown(
                id='analytics-selector-dropdown',
                options=[{'label': i.replace('_', ' '), 'value': i} for i in sample_df.columns.values[1::]],
                className='four columns',
                value='Monthly_Revenue'),


            html.Div([analyze_metric(sample_df, keyword = "Monthly_Revenue", print_word = "monthly revenue")],
                className="four columns", id='analytics-data-output')
            
        ], className='row'),
    ])
])

def process_new_df(content, filename):
    
    content_type, content_string = content.split(',')
    decoded = base64.b64decode(content_string)

    try:
        # Will only work with csv
        uploaded_df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])


    return uploaded_df

#Output('output-data-upload', 'children'),

@app.callback([Output('header-desc-text', 'children'),
              Output('analytics-data-output', 'children'),
              Output('pie-chart-selector-dropdown', 'options'),
              Output('net-income-line-chart', 'figure'),
              Output('monthly-revenue-bar-chart', 'figure'),
              Output('revenue-per-hour-line-chart', 'figure'),
              Output('assets-capital-bar-chart', 'figure'),
              Output('expenses-proportion-pie-chart', 'figure'),
              Output('revenue-proportion-pie-chart', 'figure')],
              [Input('pie-chart-selector-dropdown', 'value'),
              Input('analytics-selector-dropdown', 'value'),
              Input('upload-data', 'contents')],
              [State('upload-data', 'filename')])
def update_output(value, analytic_value, content, filename):


    if filename is None:
        filename = 'My Sample Cupcake Shop.csv'

    if content is not None:
        t_df = process_new_df(content, filename)    
    else:
        t_df = pd.read_csv('data/sample_data.csv')

    just_file_name = filename.split(".")[0]

    new_header_desc = html.H5(just_file_name, id='header-desc-text')

    kw_output = ''
    for i in analytic_value.split('_'):
        kw_output+= (i[0].lower()+i[1:]+" ")
        
    new_analytics_data_output = analyze_metric(t_df, analytic_value, kw_output[:-1])

    new_pie_chart_dropdown_options = [{'label': date_obj_from_iso_str(i).strftime('%b %Y'), 'value': i} for i in t_df['Date'].unique()]

    return [new_header_desc, new_analytics_data_output, new_pie_chart_dropdown_options,
            gen_net_income_line_chart(t_df), gen_monthly_revenue_bar_chart(t_df),
            gen_revenue_per_hour_line_chart(t_df), gen_assets_capital_bar_chart(t_df),
            gen_expenses_proportion_pie_chart(t_df, month=value), gen_revenue_proportion_pie_chart(t_df, month=value)]



if __name__ == '__main__':
    app.run_server(debug=True)

