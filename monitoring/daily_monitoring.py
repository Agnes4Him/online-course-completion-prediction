import datetime
import time
import psycopg

from evidently import ColumnMapping
from evidently.report import Report
from evidently.metrics import ColumnDriftMetric, DatasetDriftMetric, DatasetMissingValuesMetric

from prefect import flow, task

def monitor_data(target, numerical, categorical, reference_data, current_data):
    column_mapping = ColumnMapping(
        target=target,
        prediction='prediction',
        numerical_features=numerical,
        categorical_features=categorical
    )

    report = Report(metrics=[
        ColumnDriftMetric(column_name='prediction'),
        DatasetDriftMetric(),
        DatasetMissingValuesMetric()
        ]
    )

    report.run(reference_data=reference_data, current_data=current_data, column_mapping=column_mapping)

    result = report.as_dict()

    return result