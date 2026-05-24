from flask import Flask, render_template, request, jsonify
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

# ------------------------------------------
# FLASK APP
# ------------------------------------------

app = Flask(__name__)
# ------------------------------------------
# LOAD DATASET
# ------------------------------------------

df = pd.read_csv('data.csv')

# ------------------------------------------
# ENCODE CATEGORICAL COLUMNS
# ------------------------------------------

categorical_cols = [
    'Sex',
    'ChestPainType',
    'RestingECG',
    'ExerciseAngina',
    'ST_Slope'
]
encoders = {}

for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le

# ------------------------------------------
# FEATURES AND TARGET
# ------------------------------------------

X = df.drop('HeartDisease', axis=1)
y = df['HeartDisease']

# ------------------------------------------
# TRAIN TEST SPLIT
# ------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# ------------------------------------------
# TRAIN MODEL
# ------------------------------------------

model = RandomForestClassifier()
model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)

# ------------------------------------------
# HOME PAGE
# ------------------------------------------

@app.route('/')
def home():
    return render_template('index.html', accuracy=round(accuracy * 100, 2))

# ------------------------------------------
# PREDICTION ROUTE
# ------------------------------------------

@app.route('/predict', methods=['POST'])
def predict():

    data = request.json

    input_data = pd.DataFrame({
        'ChestPainType': [data['chestPain']],
        'RestingBP': [int(data['restingBP'])],
        'Cholesterol': [int(data['cholesterol'])],
        'FastingBS': [int(data['fastingBS'])],
        'RestingECG': [data['restingECG']],
        'MaxHR': [int(data['maxHR'])],
        'ExerciseAngina': [data['exerciseAngina']],
        'Oldpeak': [float(data['oldpeak'])],
        'ST_Slope': [data['stSlope']]
    })
    # Encode input
    for col in categorical_cols:
        input_data[col] = encoders[col].transform(input_data[col])

    # Predict
    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]

    if prediction == 1:
        result = 'High Risk of Heart Disease'
    else:
        result = 'Low Risk of Heart Disease'

    return jsonify({
        'prediction': result,
        'probability': round(probability * 100, 2)
    })

# ----------------------------------# RUN APP
# ------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)