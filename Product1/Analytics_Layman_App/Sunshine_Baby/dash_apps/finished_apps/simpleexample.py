import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
import plotly.express as px


from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange
from google.analytics.data_v1beta.types import Dimension
from google.analytics.data_v1beta.types import Metric
from google.analytics.data_v1beta.types import RunReportRequest
from google.analytics.data_v1beta.types import OrderBy
import pandas as pd
import numpy as np
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=r'C:\Users\Rahul\Desktop\rising-ethos-389717-e8b5769736f0.json'
property_id = '311880004'
client = BetaAnalyticsDataClient()


request = RunReportRequest(
        property='properties/'+property_id,
        dimensions=[Dimension(name="date")],
        metrics=[Metric(name="sessions")],
        date_ranges=[DateRange(start_date="2023-06-01", end_date="today")],
    )



def format_report(request):
    response = client.run_report(request)

    # Row index
    row_index_names = [header.name for header in response.dimension_headers]
    dim_values = []
    for i in range(len(row_index_names)):
        dim_values.append([row.dimension_values[i].value for row in response.rows])

    # Row flat data
    metric_names = [header.name for header in response.metric_headers]
    data_values = []
    for i in range(len(metric_names)):
        data_values.append([row.metric_values[i].value for row in response.rows])

    output = pd.DataFrame(data=np.transpose(np.array(data_values, dtype='f')),
                          columns=metric_names)
    out = pd.DataFrame(data=np.transpose(np.array(dim_values)), columns=row_index_names)

    return pd.concat([out, output], axis=1)



data=format_report(request)
data['date'] = pd.to_datetime(data['date'])
sorted_data = data.sort_values(by='date', ascending=True)
request = RunReportRequest(
        property='properties/'+property_id,
        dimensions=[Dimension(name="landingPage")],
        metrics=[Metric(name="screenPageViews")],
        date_ranges=[DateRange(start_date="2023-06-01", end_date="today")],
    )
data2=format_report(request)
data2_sorted = data2.sort_values(by='screenPageViews', ascending=False)
data2_sorted_10=data2_sorted.head(8)


app = DjangoDash('SimpleExample')


fig = px.line(sorted_data, x="date", y="sessions", title='Sessions Over Time')
fig2= px.bar(data2_sorted_10, x='landingPage', y='screenPageViews')

app.layout = html.Div(children=[
    dcc.Graph(
        id='life-exp-vs-gdp',
        figure=fig,style={'width': '40vh', 'height': '30vh'}
    ),html.Div(children=[
        dcc.Graph(
            id='bar_plot_data',
            figure=fig2,style={'width': '80vh', 'height': '60vh'}

        )
    ])
])


