from flask import Flask, render_template, request
import pandas as pd
from project import accuracy
from predict import predict_student

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():

    student_id = int(request.form["student_id"])
    attendance = float(request.form["attendance"])
    internal = float(request.form["internal"])
    assignment = float(request.form["assignment"])
    study = float(request.form["study"])
    participation = float(request.form["participation"])

    prediction, suggestions = predict_student(
        student_id, attendance, internal, assignment, study, participation
    )

    return render_template(
        "result.html",
        student_id=student_id,
        prediction=prediction,
        suggestions=suggestions
    )

@app.route("/history/<int:student_id>")
def history(student_id):

    df = pd.read_csv("student_history.csv")

    student = df[df["student_id"] == student_id]

    records = student.to_dict(orient="records")

    return render_template(
        "history.html",
        student_id=student_id,
        records=records
    )

@app.route("/dashboard")
def dashboard():

    df = pd.read_csv("student_history.csv")

    # Top students
    top = df.sort_values(by="final_score", ascending=False).head(5)

    students = top["student_id"].tolist()
    scores = top["final_score"].tolist()

    # Performance distribution
    excellent = len(df[df["final_score"] >= 85])
    good = len(df[(df["final_score"] >= 70) & (df["final_score"] < 85)])
    average = len(df[(df["final_score"] >= 50) & (df["final_score"] < 70)])
    poor = len(df[df["final_score"] < 50])

    values = [excellent, good, average, poor]

    return render_template(
        "dashboard.html",
        accuracy=accuracy,
        students=students,
        scores=scores,
        values=values,
        table=top.to_dict(orient="records")
    )

if __name__ == "__main__":
    app.run(debug=True)

