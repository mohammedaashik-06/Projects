# Student Performance Prediction

A Flask-based web application that predicts student performance using machine learning models. The system analyzes various academic factors to predict final scores and provides personalized suggestions for improvement.

## Features

- **Score Prediction**: Predict student final scores based on academic metrics
- **Model Comparison**: Compare multiple ML algorithms (Linear Regression, Random Forest, SVM)
- **Dashboard**: Visual analytics with performance distribution charts and top students
- **Student History**: Track individual student performance over time with trend charts
- **Improvement Suggestions**: Personalized recommendations based on prediction results

## Tech Stack

- **Backend**: Python, Flask
- **Machine Learning**: Scikit-learn (Linear Regression, Random Forest, SVR)
- **Frontend**: HTML, CSS, JavaScript
- **Data Visualization**: Chart.js
- **Data Storage**: CSV (student_history.csv)

## Project Structure

```
Student Performance Pridiction/
├── app.py                 # Flask web application
├── project.py             # ML model training and evaluation
├── predict.py             # Prediction logic
├── student_history.csv    # Historical student data
├── student_model.pkl      # Trained model (serialized)
├── model_accuracies.pkl   # Model accuracy scores
├── templates/
│   ├── index.html         # Home/Prediction form
│   ├── result.html        # Prediction results
│   ├── dashboard.html     # Analytics dashboard
│   └── history.html       # Student history view
└── README.md              # Project documentation
```

## Input Parameters

The prediction model uses the following features:

| Parameter | Description |
|-----------|-------------|
| Student ID | Unique identifier for the student |
| Attendance | Attendance percentage (0-100) |
| Internal Marks | Internal assessment score |
| Assignment Score | Assignment/submission score |
| Study Hours | Hours spent studying per day |
| Participation | Class participation rating (1-5) |

## Machine Learning Models

The project implements and compares three ML algorithms:

1. **Linear Regression**: Simple baseline model
2. **Random Forest**: Ensemble method (used as primary model)
3. **Support Vector Regression (SVR)**: Kernel-based regression

Model accuracies are evaluated using R² score and displayed on the dashboard.

## How to Run

1. Install required dependencies:
```bash
pip install flask pandas scikit-learn
```

2. Run the Flask application:
```bash
python app.py
```

3. Open your browser and navigate to:
```
http://127.0.0.1:5000
```

## Application Routes

| Route | Description |
|-------|-------------|
| `/` | Home page with prediction form |
| `/predict` | POST endpoint for score prediction |
| `/dashboard` | Analytics dashboard with charts |
| `/history/<student_id>` | Individual student history |

## Dashboard Features

- **Model Accuracy Cards**: Display R² scores for each ML model
- **Performance Distribution Pie Chart**: Shows percentage of students in each category (Excellent, Good, Average, Poor)
- **Top Students Bar Chart**: Visualizes top 5 performing students
- **Top Students Table**: Lists top students by final score

## Prediction Output

The prediction result includes:
- **Predicted Score**: Estimated final score based on input parameters
- **Suggestions**: Personalized recommendations such as:
  - Improve attendance
  - Focus on internal marks
  - Increase study hours
  - Participate more in class

## Data Format

The `student_history.csv` file contains:
```
student_id, attendance, internal_marks, assignment_score, study_hours, participation, final_score
```

## License

This project is for educational purposes.

