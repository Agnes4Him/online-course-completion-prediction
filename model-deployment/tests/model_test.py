import predict

def test_transform():
    data = {
    "UserID": 6001,
    "CourseCategory": "Science",
    "DeviceType": 1,
    "TimeSpentOnCourse": 42.233124,
    "NumberOfVideosWatched": 8,
    "NumberOfQuizzesTaken": 7
    }

    actual_data = predict.prepare_data(data)

    expected_data = {
    "UserID": 6001,
    "CourseCategory": "Science",
    "DeviceType": 1,
    "TimeSpentOnCourse": 42.23,
    "NumberOfVideosWatched": 8,
    "NumberOfQuizzesTaken": 7
    }

    assert actual_data == expected_data

# following have be provided as environment variable on the terminal before running pytest/tests command... 
# TRACKING_URI, EXPERIMENT, RUN_ID