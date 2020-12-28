import io
from base64 import b64encode

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

from kafka import KafkaConsumer
from json import loads




# for message in consumer:
#     print(message)
#     print(message.value)


buffer = io.StringIO()
df = px.data.iris()
fig = px.scatter(
    df, x="sepal_width", y="sepal_length", 
    color="species")
fig.write_html(buffer)

html_bytes = buffer.getvalue().encode()
encoded = b64encode(html_bytes).decode()

app = dash.Dash(__name__)
app.layout = html.Div([
    dcc.Graph(id="graph", figure=fig),

    html.Div(children=' ABC'),

    html.Div(id='live-update-text', children=[]),

    dcc.Interval(
            id='interval-component',
            interval=10*1000, # in milliseconds
            n_intervals=0)
])


@app.callback(Output('live-update-text', 'children'),
              Input('interval-component', 'n_intervals'))
def update_metrics(n):

    consumer = KafkaConsumer(
        'test1',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        auto_commit_interval_ms=1000,
        group_id='counters',
        value_deserializer=lambda x: loads(x.decode('utf-8')))

    result = 'INPUT'

    for message in consumer:
        result = result + str(message.value)
    print(result)
    return html.Div(n)

if __name__ == "__main__":           
    app.run_server(debug=True)