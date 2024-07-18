import os

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

print('Model loaded')
def predict(features):
    pred = model.predict(features)
    return int(pred[0])


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