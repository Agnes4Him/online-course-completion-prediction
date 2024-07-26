import os
import datetime
import psycopg

import pandas as pd

from evidently import ColumnMapping
from evidently.report import Report
from evidently.metrics import ColumnDriftMetric, DatasetDriftMetric, DatasetMissingValuesMetric

from prefect import flow, task

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

create_table_statement = """
create table if not exists metrics(
	timestamp timestamp,
	prediction_drift float,
	num_drifted_columns integer,
	share_missing_values float
)
"""

@task
def get_reference_data(file_path):
     reference_data = pd.read_parquet(file_path)
     return reference_data
     

@task
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

@task
def get_db_data():
    conn = psycopg.connect('')

    query = 'SELECT * FROM course'

    cur = conn.cursor()
    cur.execute(query)

    data = cur.fetchall()

    for item in data:
        del item['timestamp']
    print(data)

    columns = ['UserID', 'DeviceType', 'CourseCategory', 'TimeSpentOnCourse', 'NumberOfVideosWatched', 'NumberOfQuizzesTaken', 'prediction']
    df = pd.DataFrame(data, columns=columns)

    return df

@task
def prep_db():
     pass

@task
def save_metrics(report):
    timestamp = datetime.datetime.now()
    prediction_drift = report['metrics'][0]['result']['drift_score']
    num_drifted_columns = report['metrics'][1]['result']['number_of_drifted_columns']
    share_missing_values = report['metrics'][2]['result']['current']['share_of_missing_values']

    with psycopg.connect("host={} port={} dbname={} user={} password={}".format(DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD), autocommit=True) as conn:
          with conn.cursor() as curr:
                curr.execute(create_table_statement)
                curr.execute(
                    "insert into metrics(timestamp, prediction_drift, num_drifted_columns, share_missing_values) values (%s, %s, %s, %s)",
                    (timestamp, prediction_drift, num_drifted_columns, share_missing_values)
                )

@flow(log_prints=True)
def main(file_path):
    target = 'CourseCompletion'
    numerical = ['TimeSpentOnCourse', 'NumberOfVideosWatched', 'NumberOfQuizzesTaken']
    categorical = ['DeviceType', 'CourseCategory']
    current_data = get_db_data()
    reference_data = get_reference_data(file_path)
    report = monitor_data(target, numerical, categorical, reference_data, current_data)
    save_metrics(report)


if __name__ == "__main__":
    file_path = '../mlpipeline/monitoring_data/online_course_engagement_va_data.parquet'
    main(file_path)
