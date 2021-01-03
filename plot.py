import io
from base64 import b64encode
import copy
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

from kafka import KafkaConsumer
from json import loads
import pandas as pd



class Konsument():
    def __init__(self):
        self.consumer = KafkaConsumer(
                        'btc001',
                        bootstrap_servers=['localhost:9092'],
                        auto_offset_reset='earliest',
                        enable_auto_commit=True,
                        auto_commit_interval_ms=1000,
                        group_id='counters',
                        value_deserializer=lambda x: loads(x.decode('utf-8')))
        

    def get_messages(self):

        msg = next(self.consumer)
        msg = msg.value

        for k, i in msg.items():
            setattr(self, k, i)
        print(self.__dict__, flush=True)
        return msg

    def update_dataframe(self, df):
        max_idx = int(len(df))
        print('max_idx', max_idx)
        df.loc[max_idx] = [self.datetime, self.USD, self.PLN]
        print(df.tail(5), flush=True)

k = Konsument()


buffer = io.StringIO()

trading_df = pd.DataFrame(columns=['datetime', 'USD', 'PLN'])


fig_usd = px.line(
    trading_df, x="datetime", y="USD")
fig_usd.write_html(buffer)

fig_pln = px.line(
    trading_df, x="datetime", y="PLN")
fig_pln.write_html(buffer)


html_bytes = buffer.getvalue().encode()
encoded = b64encode(html_bytes).decode()

app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1(children='Big Data Project'),
    html.H2(children='Student: Jakub Sypniewski, ID: 73030'),


    html.Div(children='BTC/USD: '),
    dcc.Graph(id="graph-usd", figure=fig_usd),

    html.Div(children='BTC/PLN: '),
    dcc.Graph(id="graph-pln", figure=fig_pln),

    html.Div(children='Numer iteracji: '),
    html.Div(id='empty', children=[]),
    html.Div(id='live-update-text', children=[]),

    dcc.Interval(
            id='interval-component',
            interval=5*1000, # in milliseconds
            n_intervals=0)
])





@app.callback(Output('live-update-text', 'children'),
              Input('interval-component', 'n_intervals'))
def update_metrics(n):

    result = str(k.get_messages())
    k.update_dataframe(trading_df)
    print(result, flush=True)
    # return html.Div(n)

@app.callback(Output('empty', 'children'),
              Input('interval-component', 'n_intervals'))
def update_metrics(n):

    return html.Div(n)

@app.callback(Output('graph-usd', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live_usd(n):
    fig_usd = px.line(
        trading_df, x="datetime", y="USD")
    fig_usd.write_html(buffer)
    return fig_usd

@app.callback(Output('graph-pln', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live_pln(n):
    fig_pln = px.line(
        trading_df, x="datetime", y="PLN")
    fig_pln.write_html(buffer)
    return fig_pln





if __name__ == "__main__":           
    app.run_server(debug=True)