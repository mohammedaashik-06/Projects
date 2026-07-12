from project import model

def predict_student(student_id,attendance,internal,assignment,study,participation):

    score = model.predict([[attendance,internal,assignment,study,participation]])[0]

    suggestions = []

    if attendance < 75:
        suggestions.append("Improve attendance")

    if internal < 35:
        suggestions.append("Improve internal marks")

    if assignment < 15:
        suggestions.append("Focus more on assignments")

    if study < 3:
        suggestions.append("Increase study hours")

    if participation < 3:
        suggestions.append("Participate more in class")

    return round(score,2), suggestions
