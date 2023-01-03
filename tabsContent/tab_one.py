import pandas as pd
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import plotly.graph_objs as go
from google.oauth2 import service_account
import pandas_gbq as pd1
from app import app

layout_tab_one = html.Div([

    dcc.Interval(id='update_value1',
                 interval=1 * 5000,
                 n_intervals=0),

    html.Div([
        dcc.Graph(id='line_chart1',
                  config={'displayModeBar': False},
                  className='chart_size'),
    ], className='chart_row_center')
])


@app.callback(Output('line_chart1', 'figure'),
              [Input('update_value1', 'n_intervals')])
def line_chart_values(n_intervals):
    header = ['DateTime', 'InsideHumidity', 'InsideTemperature', 'InsideCO2',
              'OutsideHumidity', 'OutsideTemperature', 'OutsideCO2']
    df = pd.read_csv('data1.csv', names=header)
    df.drop_duplicates(keep=False, inplace=True)

    return {
        'data': [go.Scatter(
            x=df['DateTime'].tail(30),
            y=df['OutsideTemperature'].tail(30),
            mode='markers+lines',
            line=dict(width=3, color='#ffbf00'),
            marker=dict(size=7, symbol='circle', color='#ffbf00',
                        line=dict(color='#ffbf00', width=2)
                        ),
            hoverinfo='text',
            hovertext=
            '<b>Date Time</b>: ' + df['DateTime'].tail(30).astype(str) + '<br>' +
            '<b>Temperature (°C)</b>: ' + [f'{x:,.2f} °C' for x in df['OutsideTemperature'].tail(30)] + '<br>'
        )],

        'layout': go.Layout(
            plot_bgcolor='rgba(255, 255, 255, 0)',
            paper_bgcolor='rgba(255, 255, 255, 0)',
            title={
                'text': '<b>Current Temperature (°C)</b>',
                'y': 0.97,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            titlefont={
                'color': '#ffbf00',
                'size': 17},
            hovermode='x unified',
            margin=dict(t=50, r=40),
            xaxis=dict(range=[min(df['DateTime'].tail(30)), max(df['DateTime'].tail(30))],
                       title='<b>Hours</b>',
                       color='#ffffff',
                       showline=True,
                       showgrid=False,
                       linecolor='#ffffff',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Arial',
                           size=12,
                           color='#ffffff')

                       ),

            yaxis=dict(
                range=[min(df['OutsideTemperature'].tail(30)) - 0.05, max(df['OutsideTemperature'].tail(30)) + 0.05],
                title='<b>Temperature (°C)</b>',
                color='#ffffff',
                zeroline=False,
                showline=True,
                showgrid=False,
                linecolor='#ffffff',
                linewidth=1,
                ticks='outside',
                tickfont=dict(
                    family='Arial',
                    size=12,
                    color='#ffffff')

                ),
            font=dict(
                family="sans-serif",
                size=12,
                color='#ffffff')

        )

    }
