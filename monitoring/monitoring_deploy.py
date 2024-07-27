from daily_monitoring import main

from prefect.deployments import Deployment
from prefect.client.schemas.schedules import CronSchedule


deployment = Deployment.build_from_flow(
    flow=main,
    name="monitoring",
    schedules=[CronSchedule(cron="0 6 * * *", timezone="America/Chicago")],
    parameters={},
    work_queue_name="mlops-monitoring",
)

if __name__ == "__main__":
    deployment.apply()