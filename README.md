# PROJECT TITLE
Online course completion prediction

# PROBLEM DESCRIPTION

1. Introduction
Online learning platforms have revolutionized education by making a wide range of courses accessible to people worldwide. However, a significant challenge these platforms face is the high dropout rate of students. Understanding and predicting which students are likely to complete a course can help educators and administrators design better intervention strategies, personalize learning experiences, and ultimately improve student retention and success rates.

2. Objective
The objective of this project is to `train` and `deploy` a machine learning model that predicts whether a student will complete an online course. By accurately predicting course completion, the model can assist online learning platforms in identifying at-risk students early and implement measures to support them throughout their learning journey.

3. Data Source
The data for this project was sourced from kaggle.com, and includes the following:

a) UserID: Unique identifier of a student.
b) CourseCategory: Category of the course enrolled in by a student. This includes `Arts`, `Science`, `Programmming` and `Health`.
c) TimeSpentOnCourse: This is the total amount of time spent, in hours, on a course by a student.
d) NumberOfVideosWatched: This is the number of video content relating to a course that has been consumed by a student.
e) NumberOfQuizzesTaken: This is the number of quizzes relating to a course that a student has taken.
f) QuizScores: Average of the scores obtained by a student in all the quizzes taken.
g) CompletionRate: How much of a course is completed by a student.
h) DeviceType: The type of device used in taking the course. Two types were considerd in this dataset - mobile(0) or laptop(1)
i) CourseCompletion: A boolean indicating if a student completed a course (1) or not (0)

4. Methodology

a) Data Preprocessing: Cleaning and transforming the raw data, handling missing values, and encoding categorical variables.

b) Exploratory Data Analysis (EDA): Analyzing the data to identify patterns, correlations, and insights that will inform feature engineering and model selection.

c) Feature Engineering: Creating new features that capture important aspects of student behavior and engagement.

d) Model Selection: Evaluating different machine learning algorithms (e.g., logistic regression, Linear regression, Lasso) to find the best fit for the problem.

e) Model Training and Evaluation: Training the selected model on historical data and evaluating its performance using appropriate metrics (e.g., mean squared error).

f) Hyperparameter Tuning: Optimizing the model’s hyperparameters to improve its performance.

g) Deployment: Deploying the model to a web service and setting up an almost real-time prediction system.

h) Monitoring: Continuously monitoring the model’s performance to ensure its accuracy and relevance over time.

5. Expected Outcomes

** Improved Retention Rates: By predicting and addressing factors leading to dropouts, an online platform can retain more students.

** Personalized Learning: Tailoring the learning experience based on the predicted needs and behaviors of students.

** Informed Interventions: Enabling educators to proactively engage with at-risk students and provide targeted support.

** Data-Driven Insights: Gaining a deeper understanding of the factors that contribute to course completion, which can inform future course design and teaching strategies.

# ENVIRONMENT SETUP AND HOW THE CODE WORKS

There are 5 subdirectories in the root folder of the project.

** `mlpipeline` - contains directories and files needed to pull the dataset used, save the data and train a model using a pipeline and work orchestration tool

** `model-deployment` - this contains all the logic to deploy the model to a web service, apply linting and formating, and test it.

** `infrastructure` - this contains the Terraform directories and files to automate provisioning of resources needed to host the web service on the AWS Cloud platform.

** `monitoring` - this contains the script for daily monitoring of the model performance.

** `.github` - this is for GitHub CI/CD pipeline to automate the cloud deployment of of the web service and the needed infrastructures.

`mlpipeline`, `model-deployment` and `monitoring` have seperate pipenv environments.

NOTE: Everything is running locally at the moment. However, provision has been made for a transfer to the AWS cloud.

`The following tools were used`...

** `Prefect` for workflow orchestration
** `MLFlow` for experiment tracking and model registry
** `Evidently` for monitoring
** `Flask` as a web service for model deployment
** `Docker` for packaging our deployment as a conatiner
** `Kubernnetes` for orchestrating the container deployment
** `Postgres` for storing monitoring data
** `Grafana` for visualization, observability and alerting
** `Terraform` as Infrastructure as Code tool
** `GitHub Actions` for CI/CD pipeline

`To run things locally`...

`MLPipeline Phase`

1. Ensure python and pipenv are installed
2. Change directory to `mlpipeline`
3. Create the following directories - `data`, `monitoring_data` to save appropriate data for model training and monitoring
4. Run the command `pipenv install --python <your-python-version>` to install all the dependencies 
5. Start MLFlow server using the command `mlflow server --backend-store-uri sqlite:///backend.db`. This will start mlflow using sqlite database as the backend store, with the database named `backend.db` in this case. The default-artifact-root would be the local filesystem in this case.
6. Access mlflow ui at `http://localhost:5000`
7. Prefect is the workflow orchestration tool of choice in this project. 
8. To start prefect, and view flows when we train the model, run the command `prefect server start`
9. Access prefect ui at `http://localhost:4200`
10. To now deploy the pipeline to run on a scheduled basis (weekly in this case), run `python mlpipeline-deploy.py`. This file contains configurations for the deployment of the mlpipeline found in `train_model.py` to prefect
11. Then run `prefect deployment run <name-of-the-flow>/<name-of-the-deployment>` e.g `prefect deployment run run-pipeline/mlpipeline`
12. Start the prefect agent to run the pipeline flow using `prefect agent start --pool "default-agent-pool" --work-queue "mlops"` command
13. For testing, you can trigger a run manually on the prefect ui.
14. Go to mlflow ui to see that a model has been trained, and registered in the model registry, and metrics, including those for monitoring using `evidently`, have been saved.

`Model Deployment Phase`

1. Change directory to `model-deployment`
2. Run the command `pipenv install --python <your-python-version>` to install all the dependencies
3. The main code is found in `predict.py` 
4. Run the web service using `python predict.py` command.
5. Using Thunderclient or Postman, you can send request to the service at `http:localhost:9696` and see expected response.
6. Sample data that can be sent is...
{
    "UserID": 6001,
    "CourseCategory": "Science",
    "DeviceType": 1,
    "TimeSpentOnCourse": 42.238989,
    "NumberOfVideosWatched": 8,
    "NumberOfQuizzesTaken": 7
}

7. The reponse will contain the prediction as `CourseCompletion` and the `RUN_ID` of the model we used.
8. Further unit test, integration test, linting and formating can be done, all in a go using the `make` command e.g `make -d`. This will run all the commands present in the Makefile found in the index directory.
10. Note that the integration testing involves starting the docker containers as specified in the docker compose file present in the index directory. Do update the docker compose file with the values of the model `RUN_ID` and other details. Ensure the MLflow server is still running so the we service can connect to it.
11. You can access the Postgres Database via Adminer - `http://localhost:8080` to see the data that has been written to it, and visualize and perform some analytics with creation of dashboards using Grafana - `http://localhost:3000`
9. Next, create a local Kubernetes cluster using Docker Desktop, Minikube or any other tool (I used Docker Desktop)
10. Ensure the Docker daemon has been started.
11. Update the manifest files found in `k8s-local` folder to contain real values e.g image name and tag for web service deployment, pstgres password(base64 encoded)
12. Run the following in the k8s cluster - `kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.3.0/deploy/static/provider/cloud/deploy.yaml` to install ingress controller to the cluster for traffic routing.
13. In ingress.yaml file, use a FQDN of your choice (mine is model.pred.com)
14. Add this domain name to the list of domain names in the hosts file and map it to local host e.g `127.0.0.1  model.pred.com`
15. Apply the manifest files as `kubectl apply -f k8s-local`
16. Test that web service is up and running by sending requests again to `http://model.pred.com/web` using Postman or ThunderClient
17. Access the other services using their subdomain names

`Monitoring Phase`

1. Change directory to `monitoring`
2. Run the command `pipenv install --python <your-python-version>` to install all the dependencies
3. This also requires `prefect` for workflow orchestration.
4. The main code is in `daily_monitoring.py` file
5. The workflow is scheduled to run daily
6. It involves pulling the previous day's data saved in PostgreSQL database, and using `evidently`, derive some data quality metrics and save this into a different table `metrics` in the database
7. Running this workflow involves the same steps as in the `MLPipeline` phase above...

`To run things in the cloud - AWS`...

`MLPipeline Phase`

1. Provision and `EC2 instance` on AWS and attach a role to it to write to S3 `Bucket`
2. Allow SSH access on port 22 from your IP Address
3. SSH into the instance and copy the MLPipeline directory to it.
4. Install pipenv, and run `pipenv install --python <your-python-version>`
5. Start MLFlow server with - mlflow server --backend-store-uri postgres://<USERNAME>:<PASSWORD>@<HOST>:<PORT>/<DATABSE_NAME> --default-artifact-root s3://<BUCKET_NAME>
6. Create an S3 Bucket and Postgres RDS instance before step 5. Allow ingress on port 5432 from the instance security group to the databse.
7. Start prefect server as in the MLPipeline phase above

`Model Deployment Phase`

1. The model deployment phase under this section involves using `GitHub Actions` as the CI/CD tool of choice
2. The configuration files for the CI/CD is located in .github directory, which is present at the root directory
3. The flow involves ...
** Create a new git branch
** Make changes to the content of `infrastructures` or `model-deplyment` directories in the new branch
** Trigger the `pre-commit hook` when a commit is made (The pre-commit configuration file should ideally be in the root directory containing the .github directory. However, in this case, it's in `model-deployment`, since that's the directory with a pipenv environment and containing the pre-commit package. Hence, this stage of quality check is missed in this project)
** Push changes to GitHub and make a `pull request` to the main branch
** This trigger the CI pipeline to run tests and quality check on the repository as well as `terraform plan` command
** Once this pull request is merged with the main branch, CD would be trigger to run `terraform plan` again, and if successful, to apply any changes in the infrastructure
** The infrestructures that have been configured in the terraform files include - EKS cluster, ECR, PostgreSQL database
** The PostgreSQL database is to save the data that would be used for monitoring
** Visualization, analytics and dashboard creation will be done using `Grafana Cloud` 
** Simple create an account on `Grafana Cloud` and connect the PostgreSQL as a data source
** After provisioning the infrastructures, the CD pipeline will build a docker image of the web service and push it to ECR
** The Kubernetes manifest files will be automatically updated with new values and the files re-applied to the Kubernetes cluster


`Monitoring Phase`

1. This involves the same steps as in the local environment
2. The EC2 instance created earlier for experiment tracking and prefect deployment will also be used to run this workflow.