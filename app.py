import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
model_path = os.path.join(basedir, 'diabetes_model.pkl')

model = pickle.load(open(model_path, 'rb'))
try:
    model = pickle.load(open('diabetes_model.pkl', 'rb'))
except FileNotFoundError:
    print("Error: Model file not found. Please run train_model.py first.")
    exit()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        features = [float(data['preg']), float(data['glucose']), float(data['bp']),
                    float(data['skin']), float(
                        data['insulin']), float(data['bmi']),
                    float(data['pedigree']), float(data['age'])]

        final_features = [np.array(features)]

        prediction = model.predict(final_features)
        probability = model.predict_proba(final_features)

        result = "Diabetic" if prediction[0] == 1 else "Healthy"
        confidence = round(np.max(probability) * 100, 2)

        return jsonify({
            'result': result,
            'confidence': confidence
        })

    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == "__main__":
    app.run(debug=True)
