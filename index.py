from dash import html
from dash import dcc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from google.oauth2 import service_account
import pandas_gbq as pd1
from tabsContent.tab_one import layout_tab_one
from tabsContent.tab_two import layout_tab_two
from tabsContent.tab_three import layout_tab_three
from app import app

tab_style = {
    'border-top': '1px solid #ffffff',
    'border-left': '1px solid #ffffff',
    'border-right': '1px solid #ffffff',
    'border-bottom': 'none',
    'backgroundColor': 'rgba(255, 255, 255, 0)',
    'color': '#ffffff',
    'fontWeight': 'bold',
    'fontFamily': 'sans-serif',
    'height': '35px',
    'padding': '7.5px'
}

tab_selected_style = {
    'border-top': '2px solid red',
    'border-bottom': 'none',
    'border-right': 'none',
    'border-left': 'none',
    'backgroundColor': 'rgba(255, 255, 255, 0)',
    'color': '#ffffff',
    'fontWeight': 'bold',
    'fontFamily': 'sans-serif',
    'height': '35px',
    'padding': '7.5px'
}

tab_selected_style1 = {
    'border-top': '2px solid red',
    'border-bottom': 'none',
    'border-right': '1px solid #ffffff',
    'border-left': 'none',
    'backgroundColor': 'rgba(255, 255, 255, 0)',
    'color': '#ffffff',
    'fontWeight': 'bold',
    'fontFamily': 'sans-serif',
    'height': '35px',
    'padding': '7.5px'
}

app.layout = html.Div([

    dcc.Interval(id='update_value',
                 interval=1 * 4000,
                 n_intervals=0),

    html.Div([
        html.Div([
            html.Img(src=app.get_asset_url('sensor.png'),
                     style={'height': '30px'},
                     className='title_image'
                     ),
            html.Div('ARDUINO WEATHER SENSORS',
                     className='title_text')
        ], className='title_row')
    ], className='bg_title'),

    html.Div([
        html.Div([
            html.Div(id='value1',
                     className='card_size'),
            html.Div(id='value2',
                     className='card_size'),
            html.Div(id='value3',
                     className='card_size')
        ], className='value_cards_column'),
    ], className='numeric_values_container'),

    html.Div([
        html.Div([
            dcc.Tabs(id='tabs', value='tab_content_one', children=[
                dcc.Tab(label='Real Time Data', value='tab_content_one',
                        style=tab_style,
                        selected_style=tab_selected_style
                        ),
                dcc.Tab(label='Hourly Data (Line Chart)', value='tab_content_two',
                        style=tab_style,
                        selected_style=tab_selected_style
                        ),
                dcc.Tab(label='Hourly Data (Bar Chart)', value='tab_content_three',
                        style=tab_style,
                        selected_style=tab_selected_style1
                        ),
            ], className='tabs_container_width')
        ], className='tabs_container')
    ], className='display_tabs_container'),

    html.Div(id='return_tab_content', children=[])
])


@app.callback(Output('return_tab_content', 'children'),
              Input('tabs', 'value'))
def render_content(value):
    if value == 'tab_content_one':
        return layout_tab_one
    elif value == 'tab_content_two':
        return layout_tab_two
    elif value == 'tab_content_three':
        return layout_tab_three


@app.callback(Output('value1', 'children'),
              [Input('update_value', 'n_intervals')])
def update_value(n_intervals):
    if n_intervals == 0:
        raise PreventUpdate
    else:
        credentials = service_account.Credentials.from_service_account_file('weatherdata1.json')
        project_id = 'weatherdata1'
        df_sql = f"""SELECT
                 OutsideTemperature
                 FROM
                 `weatherdata1.WeatherSensorsData1.SensorsData1`
                 ORDER BY
                 DateTime DESC LIMIT 1
                 """
        df = pd1.read_gbq(df_sql, project_id=project_id, dialect='standard', credentials=credentials)
        get_temp = df['OutsideTemperature'].head(1).iloc[0]

    return [
        html.Div([
            html.Div('Temperature', className='card_title'),

            html.Div([
                html.Div([
                    html.Img(src=app.get_asset_url('thermometer.png'),
                             style={"height": "45px"},
                             ),
                ], className='image'),
                html.P('{0:,.1f} °C'.format(get_temp),
                       className='numeric_value'
                       ),
            ], className='card_row')
        ], className='header_card_row')
    ]


@app.callback(Output('value2', 'children'),
              [Input('update_value', 'n_intervals')])
def update_value(n_intervals):
    if n_intervals == 0:
        raise PreventUpdate
    else:
        credentials = service_account.Credentials.from_service_account_file('weatherdata1.json')
        project_id = 'weatherdata1'
        df_sql = f"""SELECT
                 OutsideHumidity
                 FROM
                 `weatherdata1.WeatherSensorsData1.SensorsData1`
                 ORDER BY
                 DateTime DESC LIMIT 1
                 """
        df = pd1.read_gbq(df_sql, project_id=project_id, dialect='standard', credentials=credentials)
        get_humidity = df['OutsideHumidity'].head(1).iloc[0]

    return [
        html.Div([
            html.Div('Humidity', className='card_title'),

            html.Div([
                html.Div([
                    html.Img(src=app.get_asset_url('humidity.png'),
                             style={"height": "45px"},
                             ),
                ], className='image'),
                html.P('{0:,.1f} %'.format(get_humidity),
                       className='numeric_value'
                       ),
            ], className='card_row')
        ], className='header_card_row')
    ]


@app.callback(Output('value3', 'children'),
              [Input('update_value', 'n_intervals')])
def update_value(n_intervals):
    if n_intervals == 0:
        raise PreventUpdate
    else:
        credentials = service_account.Credentials.from_service_account_file('weatherdata1.json')
        project_id = 'weatherdata1'
        df_sql = f"""SELECT
                 OutsideCO2
                 FROM
                 `weatherdata1.WeatherSensorsData1.SensorsData1`
                 ORDER BY
                 DateTime DESC LIMIT 1
                 """
        df = pd1.read_gbq(df_sql, project_id=project_id, dialect='standard', credentials=credentials)
        get_co2 = df['OutsideCO2'].head(1).iloc[0]

    return [
        html.Div([
            html.Div('Air Quality', className='card_title'),

            html.Div([
                html.Div([
                    html.Img(src=app.get_asset_url('air-quality.png'),
                             style={"height": "45px"},
                             ),
                ], className='image'),
                html.P('{0:,.0f} PPM'.format(get_co2),
                       className='numeric_value'
                       ),
            ], className='card_row')
        ], className='header_card_row')
    ]


if __name__ == '__main__':
    app.run_server(debug=True)
