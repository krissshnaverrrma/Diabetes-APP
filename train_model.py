import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle


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

with open('diabetes_model.pkl', 'wb') as file:
    pickle.dump(model, file)

print(f"Model trained with {model.score(X_test, y_test)*100:.2f}% accuracy.")
print("File 'diabetes_model.pkl' created successfully.")
