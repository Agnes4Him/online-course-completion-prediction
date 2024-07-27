import requests
from deepdiff import DeepDiff


features = {
    "UserID": 6001,
    "CourseCategory": "Science",
    "DeviceType": 1,
    "TimeSpentOnCourse": 42.238989,
    "NumberOfVideosWatched": 8,
    "NumberOfQuizzesTaken": 7
}

url = 'http://localhost:9696'
#url = 'model.pred.com/web'     # Domain name assigned to the model web service running on Kubernetes through Ingress rule

actual_response = requests.post(url, json=features)
#print(response.json())

expected_response = {
        'CourseCompletion': 0,
        'model_version': '765cadc38c2c4aeb8164eadd0f27265a'
}

diff = DeepDiff(actual_response, expected_response, significant_digits=1)
print(f'diff={diff}')

assert 'type_changes' not in diff
assert 'values_changed' not in diff
