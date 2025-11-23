"""
Symptom Mapper
Maps natural language symptoms to likely abnormal clinical parameters.
"""

class SymptomMapper:
    def __init__(self):
        # Map symptoms to likely parameter values (direction, value, severity)
        # direction: 'high' or 'low'
        # value: estimated value for estimation module
        # severity: 0-10 importance score
        self.symptom_map = {
            'chest_pain': {
                'Troponin': {'direction': 'high', 'value': 0.08, 'severity': 10},
                'C-reactive Protein': {'direction': 'high', 'value': 5.0, 'severity': 8},
                'Cholesterol': {'direction': 'high', 'value': 240, 'severity': 6},
                'LDL Cholesterol': {'direction': 'high', 'value': 160, 'severity': 6},
                'Systolic Blood Pressure': {'direction': 'high', 'value': 150, 'severity': 7}
            },
            'shortness_of_breath': {
                'Hemoglobin': {'direction': 'low', 'value': 10.0, 'severity': 8},
                'Red Blood Cells': {'direction': 'low', 'value': 3.5, 'severity': 7},
                'Heart Rate': {'direction': 'high', 'value': 110, 'severity': 6},
                'Troponin': {'direction': 'high', 'value': 0.05, 'severity': 9}
            },
            'fatigue': {
                'Hemoglobin': {'direction': 'low', 'value': 11.0, 'severity': 7},
                'Glucose': {'direction': 'high', 'value': 160, 'severity': 6}, # Could be high or low
                'HbA1c': {'direction': 'high', 'value': 6.5, 'severity': 5},
                'Thyroid': {'direction': 'abnormal', 'value': None, 'severity': 4} # Not in our model but relevant
            },
            'thirst': {
                'Glucose': {'direction': 'high', 'value': 200, 'severity': 9},
                'HbA1c': {'direction': 'high', 'value': 7.5, 'severity': 8},
                'Insulin': {'direction': 'high', 'value': 20, 'severity': 6}
            },
            'frequent_urination': {
                'Glucose': {'direction': 'high', 'value': 190, 'severity': 9},
                'HbA1c': {'direction': 'high', 'value': 7.2, 'severity': 8},
                'Creatinine': {'direction': 'high', 'value': 1.3, 'severity': 6}
            },
            'dizziness': {
                'Systolic Blood Pressure': {'direction': 'low', 'value': 90, 'severity': 7},
                'Hemoglobin': {'direction': 'low', 'value': 10.5, 'severity': 6},
                'Glucose': {'direction': 'low', 'value': 60, 'severity': 8}
            },
            'palpitations': {
                'Heart Rate': {'direction': 'high', 'value': 120, 'severity': 8},
                'Potassium': {'direction': 'low', 'value': 3.0, 'severity': 7}, # Not in model
                'Hemoglobin': {'direction': 'low', 'value': 10.0, 'severity': 6}
            },
            'pale': {
                'Hemoglobin': {'direction': 'low', 'value': 9.0, 'severity': 9},
                'Red Blood Cells': {'direction': 'low', 'value': 3.2, 'severity': 8},
                'Hematocrit': {'direction': 'low', 'value': 30, 'severity': 8}
            },
            'swelling': {
                'Creatinine': {'direction': 'high', 'value': 1.5, 'severity': 8},
                'Albumin': {'direction': 'low', 'value': 3.0, 'severity': 7}, # Not in model
                'Heart Rate': {'direction': 'high', 'value': 90, 'severity': 5}
            }
        }

    def get_implied_parameters(self, symptoms):
        """Get list of parameters implied by a list of symptoms"""
        implied_params = {}
        
        for symptom in symptoms:
            if symptom in self.symptom_map:
                for param, details in self.symptom_map[symptom].items():
                    if param not in implied_params:
                        implied_params[param] = []
                    implied_params[param].append(details)
                    
        return implied_params
