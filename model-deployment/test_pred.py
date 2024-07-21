import requests

features = {
    "UserId": 5678,
    "CourseCategory": "Programming",
    "DeviceType": 0,
    "TimeSpentOnCourse": 40.238989,
    "NumberOfVideosWatched": 8,
    "NumberOfQuizzesTaken": 3
}

url = 'http://localhost:9696/predict'
response = requests.post(url, json=features)
print(response.json())