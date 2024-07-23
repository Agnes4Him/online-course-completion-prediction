import requests

features = {
    "UserID": 8754,
    "CourseCategory": "Programming",
    "DeviceType": 0,
    "TimeSpentOnCourse": 30.238989,
    "NumberOfVideosWatched": 10,
    "NumberOfQuizzesTaken": 8
}

#url = 'http://localhost:9696/predict'
url = 'http://localhost:9696'
response = requests.post(url, json=features)
print(response.json())