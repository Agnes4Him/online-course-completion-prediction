import pandas as pd

#import pickle

from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import mean_squared_error
from sklearn.pipeline import make_pipeline

import mlflow

from evidently import ColumnMapping
from evidently.report import Report
from evidently.metrics import ColumnDriftMetric, DatasetDriftMetric, DatasetMissingValuesMetric

from prefect import flow, task


@task
def mlflow_setup():
    TRACKING_URI = "http://127.0.0.1:5000"
    EXPERIMENT = "online-course-engagement-prediction-experiment-1"

    mlflow.set_tracking_uri(TRACKING_URI)
    mlflow.set_experiment(EXPERIMENT)

@task
def read_data(file_path):
    df = pd.read_parquet(file_path)

    return df

@task
def get_train(df):
    df_train = df[:6000]

    return df_train

@task
def get_val(df):
    df_val = df[6000:]

    return df_val

def write_datasets_to_output(df_train, df_val, train_dataset_output, val_dataset_output):
    df_train.to_parquet(train_dataset_output)
    df_val.to_parquet(val_dataset_output)

@task
def prepare_train(df_train, categorical, numerical, target):    
    train_dict = df_train[categorical + numerical].to_dict(orient='records')

    y_train = df_train[target].values

    result = {'features':train_dict, 'target':y_train}

    return result

@task
def prepare_val(df_val, categorical, numerical, target):
    val_dict = df_val[categorical + numerical].to_dict(orient='records')

    y_val = df_val[target].values

    result = {'features':val_dict, 'target':y_val}

    return result

@task
def monitor_pipeline(numerical, categorical, df_train_mon, df_val_mon):
    column_mapping = ColumnMapping(
        target=None,
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

    report.run(reference_data=df_train_mon, current_data=df_val_mon, column_mapping=column_mapping)

    result = report.as_dict()

    report.save_html("./report.html")

    return result

@task
def write_monitoring_data_to_output(df_train_mon, df_val_mon, train_output, val_output):
    df_train_mon.to_parquet(train_output)
    df_val_mon.to_parquet(val_output)


@flow(log_prints=True)
def run_pipeline(file_path, train_dataset_output, val_dataset_output, train_output, val_output):
    print('setting up mlflow')
    mlflow_setup()

    categorical = ['DeviceType', 'CourseCategory']
    numerical = ['TimeSpentOnCourse', 'NumberOfVideosWatched', 'NumberOfQuizzesTaken']
    target = 'CourseCompletion'

    df = read_data(file_path)

    df_train = get_train(df)
    df_val = get_val(df)

    print(f'writing splitted datasets to {train_dataset_output} and {val_dataset_output}')
    write_datasets_to_output(df_train, df_val, train_dataset_output, val_dataset_output)

    df_train_mon = pd.DataFrame()
    df_val_mon = pd.DataFrame()

    with mlflow.start_run():
        pipeline = make_pipeline(
            DictVectorizer(),
            LogisticRegression(max_iter = 10000)
        )
        
        mlflow.set_tag("Developer", "Agnes")
        mlflow.log_param("train-data-path", "./data/online_course_engagement_train_data.csv")
        mlflow.log_param("valid-data-path", "./data/./data/online_course_engagement_val_data.csv")
        mlflow.log_param("C", 1)

        print('fetching and preparing train data')
        train = prepare_train(df_train, categorical, numerical, target)
        train_dict = train['features']
        y_train = train['target']

        print('fetching and preparing validation data')
        val = prepare_val(df_val, categorical, numerical, target)    
        val_dict = val['features']
        y_val = val['target']

        print('training LogisticRegression model')
        pipeline.fit(train_dict, y_train)

        print('making prediction on train and validation datasets')        
        val_pred = pipeline.predict(val_dict)
        train_pred = pipeline.predict(train_dict)

        print('calculating rmse for train and validation predictions')
        val_rmse = mean_squared_error(y_val, val_pred)
        train_rmse = mean_squared_error(y_train, train_pred)

        mlflow.log_metric("val_rmse", val_rmse)
        mlflow.log_metric("train_rmse", train_rmse)

        print('logging model and dictvectorizer as one artifact')    
        mlflow.sklearn.log_model(pipeline, artifact_path="model")

        print('creating new dataframes for monitoring ')
        df_val_mon['UserId'] = df_val['UserId']
        df_val_mon[categorical] = df_val[categorical]
        df_val_mon[numerical] = df_val[numerical]
        #df_val_mon[target] = df_val[target]
        df_val_mon['prediction'] = val_pred

        df_train_mon['UserId'] = df_train['UserId']
        df_train_mon[categorical] = df_train[categorical]
        df_train_mon[numerical] = df_train[numerical]
        #df_train_mon[target] = df_train[target]
        df_train_mon['prediction'] = train_pred

        print('fetching monitoring metrics')
        monitoring_metrics = monitor_pipeline(numerical, categorical, df_train_mon, df_val_mon)

        prediction_drift = monitoring_metrics['metrics'][0]['result']['drift_score']
        num_drifted_columns = monitoring_metrics['metrics'][1]['result']['number_of_drifted_columns']
        share_missing_values = monitoring_metrics['metrics'][2]['result']['current']['share_of_missing_values']

        print('logging monitoring metrics in mlflow')
        mlflow.log_metric("prediction_drift", prediction_drift)
        mlflow.log_metric("num_drifted_columns", num_drifted_columns)
        mlflow.log_metric("share_missing_values", share_missing_values)

        print(f'saving monitoring datasets to {train_output} and {val_output}')
        write_monitoring_data_to_output(df_train_mon, df_val_mon, train_output, val_output)


if __name__ == "__main__":
    file_path = './data/online_course_engagement_data.parquet'
    train_dataset_output = './data/online_course_engagement_train_data.parquet'
    val_dataset_output = './data/online_course_engagement_val_data.parquet'
    train_output = './monitoring_data/online_course_engagement_train_data.parquet'
    val_output = './monitoring_data/online_course_engagement_val_data.parquet'

    run_pipeline(file_path, train_dataset_output, val_dataset_output, train_output, val_output)