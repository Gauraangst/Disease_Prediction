"""
Parameter Estimator
Estimates missing clinical parameters based on symptoms, demographics, and population averages.
"""
import random

class ParameterEstimator:
    def __init__(self):
        # Healthy defaults (fallback)
        self.healthy_defaults = {
            'Glucose': 95,
            'Insulin': 12,
            'HbA1c': 5.0,
            'BMI': 22,
            'Hemoglobin': 14.5,
            'Platelets': 250000,
            'White Blood Cells': 7000,
            'Red Blood Cells': 4.8,
            'Hematocrit': 42,
            'Mean Corpuscular Volume': 90,
            'Mean Corpuscular Hemoglobin': 30,
            'Mean Corpuscular Hemoglobin Concentration': 33,
            'Systolic Blood Pressure': 115,
            'Diastolic Blood Pressure': 75,
            'Heart Rate': 72,
            'Cholesterol': 170,
            'Triglycerides': 100,
            'LDL Cholesterol': 100,
            'HDL Cholesterol': 50,
            'ALT': 25,
            'AST': 25,
            'Creatinine': 0.9,
            'Troponin': 0.01,
            'C-reactive Protein': 1.0
        }

    def estimate_missing_values(self, extracted_values, implied_params, demographics=None):
        """
        Fill in missing values using:
        1. Implied values from symptoms (if strong evidence)
        2. Demographic adjustments
        3. Healthy defaults (with slight random variation)
        """
        estimated_values = extracted_values.copy()
        
        # All required features for the model
        required_features = list(self.healthy_defaults.keys())
        
        for feature in required_features:
            if feature in estimated_values:
                continue
                
            # 1. Check if symptoms imply a value for this feature
            if feature in implied_params:
                # Take the most severe implication
                implications = implied_params[feature]
                # Sort by severity descending
                implications.sort(key=lambda x: x['severity'], reverse=True)
                
                # Use the value from the most severe symptom
                # Add some randomness so it's not identical every time
                base_value = implications[0]['value']
                estimated_values[feature] = base_value * random.uniform(0.9, 1.1)
                
            else:
                # 2. Use healthy default with variation
                base_value = self.healthy_defaults[feature]
                
                # Adjust based on demographics if available
                if demographics:
                    if feature == 'Hemoglobin' and demographics.get('sex') == 'Female':
                        base_value = 13.5 # Lower for females
                    elif feature == 'Creatinine' and demographics.get('sex') == 'Female':
                        base_value = 0.7 # Lower for females
                        
                # Add small random variation (±5%) to look natural
                estimated_values[feature] = base_value * random.uniform(0.95, 1.05)
                
        return estimated_values
