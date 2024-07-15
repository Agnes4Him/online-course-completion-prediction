# online-course-completion-prediction

# Configure MLFlow with local tracking server, sqlite database and localstack S3 bucket to log model

mlflow server --backend-store-uri sqlite:///backend.db --default-artifact-root s3://<bucket_name>
