import os
from datetime import datetime
import psycopg

import mlflow

from flask import Flask, request, jsonify


#TRACKING_URI = os.getenv('TRACKING_URI', 'http://host.docker.internal:5000') # Used in developemnt(for web service running in local K8S to access local MLFlow server)
#TRACKING_URI = os.getenv('TRACKING_URI', '<EC2 INSTANCE PUBLIC IP_ADDRESS>:<PORT>') # Used in production(for web service running on Amazon EKS to access reomote MLFlow server)
TRACKING_URI = os.getenv('TRACKING_URI')
EXPERIMENT = os.getenv('EXPERIMENT')
RUN_ID = os.getenv('RUN_ID')
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

mlflow.set_tracking_uri(TRACKING_URI)
mlflow.set_experiment(EXPERIMENT)

logged_model = f'runs:/{RUN_ID}/model'
#logged_model = f's3://<BUCKET_NAME>/1/{RUN_ID}/artifacts/model'

model = mlflow.pyfunc.load_model(logged_model)

create_table_statement = """
create table if not exists features(
	timestamp timestamp,
    user_id integer,
    device_type integer,
    course_category varchar,
    time_spent_on_course float,
	number_of_videos_watched integer,
    number_of_quizzes_taken integer,
    prediction integer
);
"""

def predict(features):
    pred = model.predict(features)
    return int(pred[0])

def prep_db():
	with psycopg.connect("host={} port={} user={} password={}".format(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD), autocommit=True) as conn:
		res = conn.execute("SELECT 1 FROM pg_database WHERE datname='course'")
		if len(res.fetchall()) == 0:
			conn.execute("create database course;")
		with psycopg.connect("host={} port={} dbname={} user={} password={}".format(DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD)) as conn:
			conn.execute(create_table_statement)

def save_features(features, prediction):
    now = datetime.now()
    user_id = features['UserID']
    device_type = features['DeviceType']
    course_category = features['CourseCategory']
    time_spent_on_course = features['TimeSpentOnCourse']
    number_of_videos_watched = features['NumberOfVideosWatched']
    number_of_quizzes_taken = features['NumberOfQuizzesTaken']

    with psycopg.connect("host={} port={} dbname={} user={} password={}".format(DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD), autocommit=True) as conn:
          with conn.cursor() as curr:
                curr.execute(
                    "insert into features(timestamp, user_id, device_type, course_category, time_spent_on_course, number_of_videos_watched, number_of_quizzes_taken, prediction) values (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (now, user_id, device_type, course_category, time_spent_on_course, number_of_videos_watched, number_of_quizzes_taken, prediction)
                )


app = Flask('course-completion-prediction')

'''@app.route('/')
def ping():
    return ('Hello from prediction model web service')'''

@app.route('/', methods=['POST'])
def predict_endpoint():
    features = request.get_json()

    pred = predict(features)

    result = {
        'CourseCompletion': pred,
        'model_version': RUN_ID
    }
    
    prep_db()

    save_features(features, pred)

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)