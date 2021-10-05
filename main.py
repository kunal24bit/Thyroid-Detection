from flask import Flask, render_template, request
import numpy as np
import pickle

app = Flask(__name__)
model = pickle.load(open('Thyroid_model.pkl', 'rb'))

@app.route('/', methods=['GET'])
def Home():
    return render_template('index.html')


@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        age = int(request.form['age'])
        sex = request.form['sex']
        if sex == "M":
            sex = 1
        else:
            sex = 0
        goitre = request.form['goitre']
        if goitre == "False":
            goitre = 1
        else:
            goitre = 0
        columns = [on_thyroxine, query_on_thyroxine, on_antithyroid_medication,
                   sick, pregnant, thyroid_surgery, I131_treatment, query_hypothyroid, query_hyperthyroid,
                   lithium, goitre, tumor, hypopituitary, psych]
        for i in columns:
            i = request.form['i']
            if i == "False":
                i = 1
            else:
                i = 0

        T3 = float(request.form['T3'])
        TT4 = float(request.form['TT4'])
        T4U = float(request.form['T4U'])
        FTI = float(request.form['FTI'])



    values = np.array([[age, sex, on_thyroxine, query_on_thyroxine, on_antithyroid_medication,
                   sick, pregnant, thyroid_surgery, I131_treatment, query_hypothyroid, query_hyperthyroid,
                   lithium, goitre,  tumor,  hypopituitary, psych, T3, TT4, T4U, FTI]])

    prediction = model.predict(values)
    if prediction == 1:
        return render_template('result.html', prediction_text="Customer is Not Satisfied")
    elif prediction == 3:
        return render_template('result.html', prediction_text="Customer is Satisfied partially")
    else:
        return render_template('result.html', prediction_text="Customer is Satisfied")
    if prediction == 0:
        return render_template('result.html', prediction_text="You do not have any Thyroid symptoms.")
    elif prediction == 1:
        return render_template('result.html', prediction_text="You have compensated hypothyroid")
    elif prediction ==2:
        return render_template('result.html', prediction_text="You have primary hypothyroid")
    else:
        return render_template('result.html', prediction_text="You have secondary hypothyroiod")


if __name__ == "__main__":
    app.run(debug=True)
