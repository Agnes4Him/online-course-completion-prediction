# PROJECT TITLE
Online course completion prediction

# PROBLEM DESCRIPTION

1. Introduction
Online learning platforms have revolutionized education by making a wide range of courses accessible to people worldwide. However, a significant challenge these platforms face is the high dropout rate of students. Understanding and predicting which students are likely to complete a course can help educators and administrators design better intervention strategies, personalize learning experiences, and ultimately improve student retention and success rates.

2. Objective
The objective of this project is to develop and deploy a machine learning model that predicts whether a student will complete an online course. By accurately predicting course completion, the model can assist online learning platforms in identifying at-risk students early and implementing measures to support them throughout their learning journey.

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

# ENVIRONMENT SETUP