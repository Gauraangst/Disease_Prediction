"""
Test cardiac marker detection through Flask app endpoint
"""
import requests
import json

# Heart disease patient data from user
prediction_data = {
    'patient_id': 'TEST_CARDIAC_001',
    'patient_name': 'Test Cardiac Patient',
    'patient_age': 55,
    'patient_sex': 'Male',
    'Glucose': 132,
    'Cholesterol': 240,
    'BMI': 29.5,
    'HbA1c': 6.8,
    'Insulin': 19,
    'Hemoglobin': 13.0,
    'Platelets': 310000,
    'White_Blood_Cells': 9500,
    'Red_Blood_Cells': 4.5,
    'Hematocrit': 40.5,
    'Mean_Corpuscular_Volume': 88,
    'Mean_Corpuscular_Hemoglobin': 29,
    'Mean_Corpuscular_Hemoglobin_Concentration': 33,
    'Systolic_Blood_Pressure': 148,
    'Diastolic_Blood_Pressure': 94,
    'Heart_Rate': 92,
    'Troponin': 0.09,  # CRITICAL: HIGH!
    'C-reactive_Protein': 8.5,  # CRITICAL: HIGH!
    'LDL_Cholesterol': 160,
    'HDL_Cholesterol': 35,
    'Triglycerides': 220,
    'ALT': 32,
    'AST': 34,
    'Creatinine': 1.2
}

# Login and create session
session = requests.Session()

# Try to register/login (may fail if user exists, that's OK)
try:
    session.post('http://localhost:5000/register', data={
        'username': 'test_cardiac',
        'email': 'test@cardiac.com',
        'password': 'testpass123',
        'confirm_password': 'testpass123'
    })
except:
    pass

# Login
response = session.post('http://localhost:5000/login', data={
    'username': 'Gauraang',  # Use existing user
    'password': 'password'
})

if 'login' in response.url.lower():
    print("❌ Could not log in. Please ensure Flask app is running and credentials are correct.")
    print("Testing without authentication...")

print("=" * 80)
print("TESTING CARDIAC MARKER DETECTION VIA FLASK APP")
print("=" * 80)

print("\nKey Cardiac Indicators:")
print(f"  Troponin: {prediction_data['Troponin']} ng/mL (normal <0.04) - CARDIAC INJURY!")
print(f"  CRP: {prediction_data['C-reactive_Protein']} mg/L (normal <1.0) - INFLAMMATION!")
print(f"  LDL: {prediction_data['LDL_Cholesterol']} mg/dL (normal <100)")
print(f"  HDL: {prediction_data['HDL_Cholesterol']} mg/dL (normal >40)")
print(f"  Systolic BP: {prediction_data['Systolic_Blood_Pressure']} mmHg (normal 90-120)")
print(f"  Triglycerides: {prediction_data['Triglycerides']} mg/dL (normal <150)")

print("\nSending prediction request...")

try:
    response = session.post(
        'http://localhost:5000/predict',
        json=prediction_data,
        headers={'Content-Type': 'application/json'}
    )
    
    if response.status_code == 200:
        result = response.json()
        
        print("\n" + "=" * 80)
        print("PREDICTION RESULTS")
        print("=" * 80)
        print(f"\nPredicted Disease: {result['prediction']}")
        print(f"Confidence: {result['confidence']:.2f}%")
        print(f"Risk Level: {result['risk_level']}")
        
        print("\nProbabilities:")
        for disease, prob in result['probabilities'].items():
            print(f"  {disease}: {prob * 100:.2f}%")
        
        print("\n" + "=" * 80)
        if result['prediction'] == 'Heart Di':
            print("✅ SUCCESS: Cardiac marker detection correctly identified Heart Disease!")
        else:
            print(f"❌ FAILED: Predicted {result['prediction']} instead of Heart Disease")
            print("   Cardiac marker detection may not have triggered (score < 60?)")
        print("=" * 80)
    else:
        print(f"\n❌ Request failed with status {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nMake sure Flask app is running:")
    print("  python3 app.py")
