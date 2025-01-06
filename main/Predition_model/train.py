import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model

# Load the saved model for prediction
ensemble_model = load_model('heartifyt.h5')

# Load and preprocess the dataset
data = pd.read_csv('framingham.csv')  # Ensure path is correct
data = data.dropna().drop_duplicates()  # Handle missing and duplicate values

# Separate features and target for scaling
X = data.iloc[:, :-1]  # Feature columns
y = data.iloc[:, -1]   # Target column (if you want to compare predictions to actual values)

# Initialize and fit the scaler
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Reshape data for CNN-GRU and DNN models
X_cnn_gru = np.reshape(X_scaled, (X_scaled.shape[0], 1, X_scaled.shape[1]))  # Shape for CNN-GRU
X_dnn = X_scaled  # DNN does not need reshaping

# Predict for each row in the dataset
predicted_probs = ensemble_model.predict([X_cnn_gru, X_dnn])

# Convert probabilities to binary predictions
predictions = (predicted_probs > 0.5).astype(int)

# Display results
results = pd.DataFrame({
    'Predicted_Probability': predicted_probs.flatten(),
    'Prediction': predictions.flatten(),
    'Actual': y.values  # Optional, only if you want to see the actual target values for comparison
})

print(results.head())  # Display first few predictions
print("\nSummary:")
print(results['Prediction'].value_counts())  # Count of each prediction class (0 = No Heart Disease, 1 = Heart Disease)
