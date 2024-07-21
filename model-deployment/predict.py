import os
from datetime import datetime
import psycopg

import mlflow

from flask import Flask, request, jsonify


#TRACKING_URI = os.getenv('TRACKING_URI', 'http://host.docker.internal:5000')
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
	prediction integer,
    course_category varchar,
    device_type integer,
    time_spent_on_course float,
	number_of_videos_watched integer,
    number_of_quizzes_taken integer
);
"""

def predict(features):
    pred = model.predict(features)
    return int(pred[0])

def prep_db():
	with psycopg.connect(f'host=${DB_HOST} port=${DB_PORT} user=${DB_USER} password=${DB_PASSWORD}', autocommit=True) as conn:
		res = conn.execute("SELECT 1 FROM pg_database WHERE datname='course'")
		if len(res.fetchall()) == 0:
			conn.execute("create database course;")
		with psycopg.connect(f'host=${DB_HOST} port=${DB_PORT} dbname=${DB_NAME} user=${DB_USER} password=${DB_PASSWORD}') as conn:
			conn.execute(create_table_statement)

def save_features(features, prediction):
    now = datetime.now()
    user_id = features['UserId']
    course_category = features['CourseCategory']
    device_type = features['DeviceType']
    time_spent_on_course = features['TimeSpentOnCourse']
    number_of_videos_watched = features['NumberOfVideosWatched']
    number_of_quizzes_taken = features['NumberOfQuizzesTaken']

    with psycopg.connect(f'host=${DB_HOST} port=${DB_PORT} dbname=${DB_NAME} user=${DB_USER} password=${DB_PASSWORD}', autocommit=True) as conn:
          with conn.cursor() as curr:
                curr.execute(
                    "insert into features(timestamp, user_id, prediction, course_category, device_type, time_spent_on_course, number_of_videos_watched, number_of_quizzes_taken) values (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (now, user_id, prediction, course_category, device_type, time_spent_on_course, number_of_videos_watched, number_of_quizzes_taken)
                )


app = Flask('course-completion-prediction')

@app.route('/predict', methods=['POST'])
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