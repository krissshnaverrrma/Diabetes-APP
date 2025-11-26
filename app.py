import pandas as pd
import numpy as np
from flask import Flask, request, jsonify, render_template
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)


print("Training Model...")
try:
    url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
    col_names = ['preg', 'glucose', 'bp', 'skin',
                 'insulin', 'bmi', 'pedigree', 'age', 'label']
    df = pd.read_csv(url, header=None, names=col_names)

    X = df.drop('label', axis=1)
    y = df['label']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)
    print("Model Trained Successfully!")
except Exception as e:
    print(f"Training Failed: {e}")
    model = None


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    if not model:
        return jsonify({'error': 'Model failed to initialize. Check server logs.'})

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

        return jsonify({'result': result, 'confidence': confidence})

    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == "__main__":
    app.run(debug=True)
