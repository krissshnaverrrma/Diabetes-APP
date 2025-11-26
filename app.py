import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)

# Load the trained model
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
        # Get JSON data from frontend
        data = request.get_json()
        
        # Convert dictionary values to a list of floats
        features = [float(data['preg']), float(data['glucose']), float(data['bp']),
                    float(data['skin']), float(data['insulin']), float(data['bmi']),
                    float(data['pedigree']), float(data['age'])]
        
        # Convert to numpy array for the model
        final_features = [np.array(features)]
        
        # Make Prediction
        prediction = model.predict(final_features) # [0] or [1]
        probability = model.predict_proba(final_features) # e.g. [[0.2, 0.8]]
        
        # Format Result
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