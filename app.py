from flask import Flask, render_template, request
import numpy as np
import pickle

app = Flask(__name__)
clf = pickle.load(open("./models/creditcardpkl.pkl", "rb"))

@app.route('/')
def home():
    return render_template('index.html')

error_message = ""
@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        msg = request.form['message']
        message = msg.split()
        if len(message) == 30:
            try:
                message = [float(x) for x in message]
                vtr = np.array(message).reshape(1, -1)
                prediction = clf.predict(vtr)
                prediction = 1 if prediction == 1 else 0
                return render_template('result.html', prediction=prediction)
            
            except ValueError as e:
                return render_template('error.html')
        else:
            error_message = "Invalid input. Please enter 30 spaced numeric values."
            return render_template('error.html', error_message=error_message)
    else:
        error_message = "Invalid request method."
        return render_template('error.html', error_message = error_message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
