"""
Test the heart disease case reported by user
"""
import sys
sys.path.insert(0, '/Users/gauraangthakkar/Desktop/folder')

from module_b_scaling_bridge import ScalingBridge
import joblib
import numpy as np

# Load model components
model = joblib.load('models/best_model.pkl')
label_encoder = joblib.load('models/label_encoder.pkl')
feature_names = joblib.load('models/feature_names.pkl')
scaling_bridge = ScalingBridge.load('models/scaling_bridge.pkl')

# Heart disease patient data from user
raw_features = {
    'Glucose': 132,
    'Cholesterol': 240,
    'BMI': 29.5,
    'HbA1c': 6.8,
    'Insulin': 19,
    'Hemoglobin': 13.0,
    'Platelets': 310000,
    'White Blood Cells': 9500,
    'Red Blood Cells': 4.5,
    'Hematocrit': 40.5,
    'Mean Corpuscular Volume': 88,
    'Mean Corpuscular Hemoglobin': 29,
    'Mean Corpuscular Hemoglobin Concentration': 33,
    'Systolic Blood Pressure': 148,
    'Diastolic Blood Pressure': 94,
    'Heart Rate': 92,
    'Troponin': 0.09,  # HIGH!
    'C-reactive Protein': 8.5,  # HIGH!
    'LDL Cholesterol': 160,
    'HDL Cholesterol': 35,
    'Triglycerides': 220,
    'ALT': 32,
    'AST': 34,
    'Creatinine': 1.2
}

# Calculate derived features
epsilon = 1e-6
raw_features['LDL_HDL_Ratio'] = raw_features['LDL Cholesterol'] / (raw_features['HDL Cholesterol'] + epsilon)
raw_features['Chol_HDL_Ratio'] = raw_features['Cholesterol'] / (raw_features['HDL Cholesterol'] + epsilon)
raw_features['Glucose_Insulin_Interaction'] = raw_features['Glucose'] * raw_features['Insulin']
raw_features['MAP'] = raw_features['Diastolic Blood Pressure'] + (1/3 * (raw_features['Systolic Blood Pressure'] - raw_features['Diastolic Blood Pressure']))

print("=" * 80)
print("TESTING HEART DISEASE CASE")
print("=" * 80)

print("\nKey Abnormal Values:")
print(f"  Troponin: {raw_features['Troponin']} (normal <0.04) - CARDIAC INJURY!")
print(f"  CRP: {raw_features['C-reactive Protein']} (normal <1.0) - INFLAMMATION!")
print(f"  Cholesterol: {raw_features['Cholesterol']} (normal 125-200)")
print(f"  LDL: {raw_features['LDL Cholesterol']} (normal <100)")
print(f"  HDL: {raw_features['HDL Cholesterol']} (normal >40)")
print(f"  Systolic BP: {raw_features['Systolic Blood Pressure']} (normal 90-120)")
print(f"  LDL/HDL Ratio: {raw_features['LDL_HDL_Ratio']:.2f} (high risk)")

# Scale features
print("\nScaling features...")
scaled_features = scaling_bridge.scale_to_array(raw_features, feature_names)

print(f"\nScaled feature array shape: {scaled_features.shape}")
print(f"Scaled values range: [{scaled_features.min():.3f}, {scaled_features.max():.3f}]")

# Make prediction
prediction_encoded = model.predict(scaled_features.reshape(1, -1))[0]
prediction = label_encoder.inverse_transform([prediction_encoded])[0]
probabilities = model.predict_proba(scaled_features.reshape(1, -1))[0]

print("\n" + "=" * 80)
print("PREDICTION RESULTS")
print("=" * 80)
print(f"\nPredicted Disease: {prediction}")
print(f"Prediction Confidence: {max(probabilities) * 100:.2f}%")

print("\nProbabilities for all classes:")
for i, class_name in enumerate(label_encoder.classes_):
    print(f"  {class_name}: {probabilities[i] * 100:.2f}%")

# Check which features might be influential
print("\n" + "=" * 80)
print("FEATURE ANALYSIS")
print("=" * 80)
print("\nTop scaled features (might indicate issues):")
feature_values = list(zip(feature_names, scaled_features))
feature_values.sort(key=lambda x: x[1], reverse=True)

print("\nHighest scaled values:")
for name, value in feature_values[:10]:
    raw_val = raw_features[name]
    print(f"  {name}: scaled={value:.3f}, raw={raw_val}")

print("\nLowest scaled values:")
for name, value in feature_values[-10:]:
    raw_val = raw_features[name]
    print(f"  {name}: scaled={value:.3f}, raw={raw_val}")

print("\n" + "=" * 80)
if prediction == "Healthy":
    print("❌ CRITICAL ERROR: Model predicted Healthy for clear heart disease case!")
    print("This is a dangerous false negative that needs immediate fixing.")
elif prediction == "Heart Di":
    print("✓ Model correctly identified heart disease")
else:
    print(f"⚠️  Model predicted {prediction} instead of Heart Disease")
print("=" * 80)
