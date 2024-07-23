# online-course-completion-prediction

# Configure MLFlow with local tracking server, sqlite database and localstack S3 bucket to log model

mlflow server --backend-store-uri sqlite:///backend.db --default-artifact-root s3://<bucket_name>

# On Linux...
gunicorn --bind=0.0.0.0:9696 predict:app

CMD ["gunicorn", "predict:app", "-b", "0.0.0.0:9696", "-w", "4"]

# On Windows
pip install waitress
waitress-serve --listen=*:9696 predict:app

docker network create front-tier

docker network create back-tier

docker build -t mlflow:1.0.0 .

docker run -d --name mlflow -p 5000:5000 --network back-tier mlflow:1.0.0

docker system prune --volumes -af

kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.3.0/deploy/static/provider/cloud/deploy.yaml