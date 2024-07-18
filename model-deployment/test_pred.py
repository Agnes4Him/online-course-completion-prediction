import requests

features = {
    "UserId": 4567,
    "CourseCategory": "Programming",
    "DeviceType": 1,
    "TimeSpentOnCourse": 15.738969,
    "NumberOfVideosWatched": 7,
    "NumberOfQuizzesTaken": 5
}

url = 'http://localhost:9696/predict'
response = requests.post(url, json=features)
print(response.json())