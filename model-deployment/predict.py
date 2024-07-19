import os
import datetime
import time
import psycopg

import mlflow

from flask import Flask, request, jsonify


TRACKING_URI = "http://127.0.0.1:5000"
EXPERIMENT = "online-course-engagement-prediction-experiment-1"

mlflow.set_tracking_uri(TRACKING_URI)
mlflow.set_experiment(EXPERIMENT)

RUN_ID = os.getenv('RUN_ID', '813bae34a9f4439d866c64223ed8146f')

logged_model = f'runs:/{RUN_ID}/model'
#logged_model = f's3://<BUCKET_NAME>/1/{RUN_ID}/artifacts/model'

model = mlflow.pyfunc.load_model(logged_model)

create_table_statement = """
create table if not exists features(
	timestamp timestamp,
	prediction integer,
	num_drifted_columns integer,
	share_missing_values float
)
"""

def predict(features):
    pred = model.predict(features)
    return int(pred[0])

def prep_db():
	with psycopg.connect("host=localhost port=5432 user=postgres password=example", autocommit=True) as conn:
		res = conn.execute("SELECT 1 FROM pg_database WHERE datname='course'")
		if len(res.fetchall()) == 0:
			conn.execute("create database test;")
		with psycopg.connect("host=localhost port=5432 dbname=course user=postgres password=example") as conn:
			conn.execute(create_table_statement)


def save_features(features, prediction):
    with psycopg.connect("host=localhost port=5432 dbname=course user=postgres password=example", autocommit=True) as conn:
          with conn.cursor() as curr:
                curr.execute(
                    "insert into features(timestamp, prediction_drift, num_drifted_columns, share_missing_values) values (%s, %s, %s, %s)",
                    (datetime, prediction, num_drifted_columns, share_missing_values)
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
    

    return jsonify(result)
    #return result


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)