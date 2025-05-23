# -*- coding: utf-8 -*-
"""Diabetes Prediction

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1oJhR1Neh2iAdeuXDZd3BczJHVAkwDq_X
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
!pip install gradio
import gradio as gr

# Load the dataset
url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
columns = ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI", "DiabetesPedigreeFunction", "Age", "Outcome"]
df = pd.read_csv(url, names=columns)

# Display first few rows
df.head()

# @title SkinThickness vs Insulin

from matplotlib import pyplot as plt
df.plot(kind='scatter', x='SkinThickness', y='Insulin', s=32, alpha=.8)
plt.gca().spines[['top', 'right',]].set_visible(False)

print(df.isnull().sum())

df.describe()

sns.countplot(x='Outcome', data=df)
plt.show()

plt.figure(figsize=(10,6))
sns.heatmap(df.corr(), annot=True, cmap="coolwarm")
plt.show()

X = df.drop("Outcome", axis=1)
y = df["Outcome"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.9, random_state=100)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

model = RandomForestClassifier(n_estimators=100, random_state=100)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Accuracy Score
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# Confusion Matrix
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Classification Report
print("Classification Report:")
print(classification_report(y_test, y_pred))

import joblib
joblib.dump(model, "diabetes_model.pkl")

loaded_model = joblib.load("diabetes_model.pkl")

sample_data = np.array([[6, 148, 72, 35, 0, 33.6, 0.627, 50]])  # Example input
sample_data = scaler.transform(sample_data)
prediction = model.predict(sample_data)

print("Diabetes Prediction:", "Positive" if prediction[0] == 1 else "Negative")

!pip install gradio

import numpy as np
import joblib

# Load your pre-trained model
model = joblib.load("diabetes_model.pkl")

# This function will take inputs and predict the diabetes risk
def predict_diabetes(blood_pressure, glucose, skin_thickness, pregnancies, insulin):
    # Prepare the data for the model (adjust based on your model's needs)
    inputs = np.array([[blood_pressure, glucose, skin_thickness, pregnancies, insulin]])

    # Get the prediction
    prediction = model.predict(inputs)

    # Return "Diabetic" or "Not Diabetic" based on the prediction
    return "Diabetic" if prediction == 1 else "Not Diabetic"

import gradio as gr
import numpy as np
import joblib

# Load the pre-trained model
model = joblib.load("diabetes_model.pkl")


def predict_diabetes(pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, dpf, age):
    # Prepare the data for the model
    inputs = np.array([[pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, dpf, age]])
    inputs = scaler.transform(inputs)  # Scale the input
    prediction = model.predict(inputs)
    return "Diabetic" if prediction[0] == 1 else "Not Diabetic"

# Define input components
demo = gr.Interface(
    fn=predict_diabetes,
    inputs=[
        gr.Number(label="Pregnancies"),
        gr.Number(label="Glucose"),
        gr.Number(label="Blood Pressure"),
        gr.Number(label="Skin Thickness"),
        gr.Number(label="Insulin"),
        gr.Number(label="BMI"),
        gr.Number(label="Diabetes Pedigree Function"),
        gr.Number(label="Age")
    ],
    outputs=gr.Textbox(label="Diabetes Prediction"),
    title="Diabetes Prediction System",
    description="Enter the medical parameters to predict diabetes risk."
)

demo.launch()