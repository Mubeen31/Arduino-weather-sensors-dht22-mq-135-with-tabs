from dash import html
from dash import dcc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import plotly.graph_objs as go
from google.oauth2 import service_account
import pandas_gbq as pd1
import pandas as pd
from app import app

layout_tab_two = html.Div([

    dcc.Interval(id='update_value2',
                 interval=1 * 11000,
                 n_intervals=0),

    html.Div([
        dcc.Graph(id='line_chart2',
                  config={'displayModeBar': False},
                  className='chart_size'),
    ], className='chart_row_center')
])


@app.callback(Output('line_chart2', 'figure'),
              [Input('update_value2', 'n_intervals')])
def line_chart_values(n_intervals):
    credentials = service_account.Credentials.from_service_account_file('weatherdata1.json')
    project_id = 'weatherdata1'
    df_sql = f"""SELECT DateTime, OutsideTemperature
                                     FROM
                                     `weatherdata1.WeatherSensorsData1.SensorsData1`
                                     ORDER BY
                                     DateTime ASC
                                     """
    df = pd1.read_gbq(df_sql, project_id=project_id, dialect='standard', credentials=credentials)
    df['DateTime'] = pd.to_datetime(df['DateTime'])
    df['Date'] = df['DateTime'].dt.date
    df['Date'] = pd.to_datetime(df['Date'])
    df['Hour'] = pd.to_datetime(df['DateTime']).dt.hour
    unique_date = df['Date'].unique()
    filter_today_date = df[df['Date'] == unique_date[-1]][['Date', 'Hour', 'OutsideTemperature']]
    today_hourly_values = filter_today_date.groupby(['Date', 'Hour'])['OutsideTemperature'].mean().reset_index()

    return {
        'data': [go.Scatter(
            x=today_hourly_values['Hour'],
            y=today_hourly_values['OutsideTemperature'],
            mode='markers+lines',
            line=dict(width=3, color='#ffbf00'),
            marker=dict(size=7, symbol='circle', color='#CA23D5',
                        line=dict(color='#CA23D5', width=2)
                        ),
            hoverinfo='text',
            hovertext=
            '<b>Date</b>: ' + today_hourly_values['Date'].astype(str) + '<br>' +
            '<b>Hour</b>: ' + today_hourly_values['Hour'].astype(str) + '<br>' +
            '<b>Temperature (°C)</b>: ' + [f'{x:,.2f} °C' for x in today_hourly_values['OutsideTemperature']] + '<br>'
        )],

        'layout': go.Layout(
            plot_bgcolor='rgba(255, 255, 255, 0)',
            paper_bgcolor='rgba(255, 255, 255, 0)',
            title={
                'text': '<b>Today Temperature (°C)</b>',
                'y': 0.97,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            titlefont={
                'color': '#ffbf00',
                'size': 17},
            hovermode='x unified',
            margin=dict(t=50, r=40),
            xaxis=dict(
                tick0=0,
                dtick=1,
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
