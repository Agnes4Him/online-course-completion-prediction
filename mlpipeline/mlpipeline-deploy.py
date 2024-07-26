from train_model import run_pipeline
from prefect.deployments import Deployment
#from prefect.server.schemas.schedules import CronSchedule
from prefect.client.schemas.schedules import CronSchedule

file_path = './data/online_course_engagement_data.parquet'
train_dataset_output = './data/online_course_engagement_train_data.parquet'
val_dataset_output = './data/online_course_engagement_val_data.parquet'
train_output = './monitoring_data/online_course_engagement_train_data.parquet'
val_output = './monitoring_data/online_course_engagement_val_data.parquet'

deployment = Deployment.build_from_flow(
    flow=run_pipeline,
    name="mlpipeline",
    #schedules=[CronSchedule(cron="0 0 * * 0", timezone="America/Chicago")],
    schedules=[CronSchedule(cron="*/2 * * * *", timezone="America/Chicago")],
    parameters={"file_path": "./data/online_course_engagement_data.parquet",
                "train_dataset_output": "./data/online_course_engagement_train_data.parquet",
                "val_dataset_output": "./data/online_course_engagement_val_data.parquet",
                "train_output": "./monitoring_data/online_course_engagement_train_data.parquet",
                "val_output": "./monitoring_data/online_course_engagement_val_data.parquet",
                "model": "online-course-model",
                "TRACKING_URI": "http://127.0.0.1:5000",
                "EXPERIMENT": "online-course-engagement-prediction-experiment"
                },
    work_queue_name="mlops",
)

if __name__ == "__main__":
    deployment.apply()