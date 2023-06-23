from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange
from google.analytics.data_v1beta.types import Dimension
from google.analytics.data_v1beta.types import Metric
from google.analytics.data_v1beta.types import RunReportRequest
from google.analytics.data_v1beta.types import OrderBy
import pandas as pd
import numpy as np
import os
import  time

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]='rising-ethos-389717-e8b5769736f0.json'
property_id = '311880004'
client = BetaAnalyticsDataClient()


request=RunReportRequest(
    property='properties/'+property_id,
    dimensions=[
                Dimension(name="language"),
                Dimension(name="deviceModel"),
                Dimension(name="eventName"),
                Dimension(name="browser"),
                Dimension(name="deviceCategory"),
                Dimension(name="continent")],



    metrics=[Metric(name="averageSessionDuration"),
             Metric(name="active28DayUsers"),
             Metric(name="active7DayUsers"),
             Metric(name='activeUsers'),
             Metric(name="adUnitExposure"),


             Metric(name="engagementRate"),
             Metric(name="sessions"),
             Metric(name="transactions"),
             Metric(name="totalUsers"),




             ],

    date_ranges=[DateRange(start_date="2023-01-01",end_date="today")],

)
print(request)


request1=RunReportRequest(
    property='properties/'+property_id,
    dimensions=[
                 Dimension(name="city"),
                 Dimension(name="cityId"),
                 Dimension(name="date"),
                 Dimension(name="day"),
                 Dimension(name="deviceModel"),





                Dimension(name="country")],




    metrics=[Metric(name="averageSessionDuration"),
             Metric(name="active28DayUsers"),
             Metric(name="active7DayUsers"),
             Metric(name='activeUsers'),
             Metric(name="adUnitExposure"),


             Metric(name="engagementRate"),
             Metric(name="sessions"),
             Metric(name="transactions"),
             Metric(name="totalUsers"),




             ],

    date_ranges=[DateRange(start_date="2023-01-01",end_date="today")],

)
print(request1)

def format_report(request):
    response = client.run_report(request)

    # Row index
    row_index_names = [header.name for header in response.dimension_headers]

    row_header = []
    for i in range(len(row_index_names)):
        row_header.append([row.dimension_values[i].value for row in response.rows])

    row_index_named = pd.MultiIndex.from_arrays(np.array(row_header), names=np.array(row_index_names))
    # Row flat data
    metric_names = [header.name for header in response.metric_headers]
    data_values = []
    for i in range(len(metric_names)):
        data_values.append([row.metric_values[i].value for row in response.rows])

    output = pd.DataFrame(data=np.transpose(np.array(data_values, dtype='f')),
                          index=row_index_named, columns=metric_names)
    return output
print(format_report(request))
print(format_report(request1))