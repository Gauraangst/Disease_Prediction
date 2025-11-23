"""
Medical NLP Extractor
Extracts clinical values and symptoms from natural language text using regex and keyword matching.
"""
import re

class MedicalNLPExtractor:
    def __init__(self):
        # Regex patterns for clinical parameters
        # Updated to be more flexible with intervening words
        self.patterns = {
            'Glucose': [r'glucose(?: level| value)?\s*(?:is|:|=)?\s*(\d+)', r'sugar(?: level)?\s*(?:is|:|=)?\s*(\d+)'],
            'Cholesterol': [r'cholesterol(?: level)?\s*(?:is|:|=)?\s*(\d+)', r'total cholesterol\s*(?:is|:|=)?\s*(\d+)'],
            'BMI': [r'bmi\s*(?:is|:|=)?\s*(\d+(?:\.\d+)?)', r'body mass index\s*(?:is|:|=)?\s*(\d+(?:\.\d+)?)'],
            'HbA1c': [r'hba1c(?: level)?\s*(?:is|:|=)?\s*(\d+(?:\.\d+)?)', r'a1c\s*(?:is|:|=)?\s*(\d+(?:\.\d+)?)'],
            'Insulin': [r'insulin(?: level)?\s*(?:is|:|=)?\s*(\d+(?:\.\d+)?)'],
            'Hemoglobin': [r'hemoglobin(?: level)?\s*(?:is|:|=)?\s*(\d+(?:\.\d+)?)', r'hb\s*(?:is|:|=)?\s*(\d+(?:\.\d+)?)'],
            'Platelets': [r'platelets(?: count)?\s*(?:is|:|=)?\s*(\d+(?:,\d+)?)', r'plt\s*(?:is|:|=)?\s*(\d+(?:,\d+)?)'],
            'White Blood Cells': [r'white blood cells(?: count)?\s*(?:is|:|=)?\s*(\d+(?:,\d+)?)', r'wbc\s*(?:is|:|=)?\s*(\d+(?:,\d+)?)'],
            'Red Blood Cells': [r'red blood cells(?: count)?\s*(?:is|:|=)?\s*(\d+(?:\.\d+)?)', r'rbc\s*(?:is|:|=)?\s*(\d+(?:\.\d+)?)'],
            'Hematocrit': [r'hematocrit(?: level)?\s*(?:is|:|=)?\s*(\d+(?:\.\d+)?)', r'hct\s*(?:is|:|=)?\s*(\d+(?:\.\d+)?)'],
            'Mean Corpuscular Volume': [r'mcv\s*(?:is|:|=)?\s*(\d+(?:\.\d+)?)'],
            'Mean Corpuscular Hemoglobin': [r'mch\s*(?:is|:|=)?\s*(\d+(?:\.\d+)?)'],
            'Mean Corpuscular Hemoglobin Concentration': [r'mchc\s*(?:is|:|=)?\s*(\d+(?:\.\d+)?)'],
            'Systolic Blood Pressure': [r'systolic(?: bp)?\s*(?:is|:|=)?\s*(\d+)', r'bp(?: is)?\s*(\d+)/\d+'],
            'Diastolic Blood Pressure': [r'diastolic(?: bp)?\s*(?:is|:|=)?\s*(\d+)', r'bp(?: is)?\s*\d+/(\d+)'],
            'Heart Rate': [r'heart rate\s*(?:is|:|=)?\s*(\d+)', r'pulse\s*(?:is|:|=)?\s*(\d+)', r'bpm\s*(?:is|:|=)?\s*(\d+)'],
            'Troponin': [r'troponin(?: level)?\s*(?:is|:|=)?\s*(\d+(?:\.\d+)?)'],
            'C-reactive Protein': [r'crp(?: level)?\s*(?:is|:|=)?\s*(\d+(?:\.\d+)?)', r'c-reactive protein\s*(?:is|:|=)?\s*(\d+(?:\.\d+)?)'],
            'LDL Cholesterol': [r'ldl(?: cholesterol)?(?: level)?\s*(?:is|:|=)?\s*(\d+)', r'bad cholesterol\s*(?:is|:|=)?\s*(\d+)'],
            'HDL Cholesterol': [r'hdl(?: cholesterol)?(?: level)?\s*(?:is|:|=)?\s*(\d+)', r'good cholesterol\s*(?:is|:|=)?\s*(\d+)'],
            'Triglycerides': [r'triglycerides(?: level)?\s*(?:is|:|=)?\s*(\d+)', r'trigs\s*(?:is|:|=)?\s*(\d+)'],
            'ALT': [r'alt(?: level)?\s*(?:is|:|=)?\s*(\d+)', r'sgpt\s*(?:is|:|=)?\s*(\d+)'],
            'AST': [r'ast(?: level)?\s*(?:is|:|=)?\s*(\d+)', r'sgot\s*(?:is|:|=)?\s*(\d+)'],
            'Creatinine': [r'creatinine(?: level)?\s*(?:is|:|=)?\s*(\d+(?:\.\d+)?)']
        }
        
        # Symptom keywords
        self.symptoms = {
            'chest_pain': ['chest pain', 'chest discomfort', 'angina', 'tightness in chest', 'heart hurts'],
            'shortness_of_breath': ['shortness of breath', 'breathless', 'difficulty breathing', 'dyspnea', 'cant breathe'],
            'fatigue': ['tired', 'fatigue', 'exhausted', 'weak', 'low energy', 'lethargic'],
            'dizziness': ['dizzy', 'lightheaded', 'faint', 'spinning'],
            'thirst': ['thirsty', 'dry mouth', 'drinking water', 'polydipsia'],
            'frequent_urination': ['urinating', 'peeing', 'bathroom', 'polyuria'],
            'palpitations': ['palpitations', 'heart racing', 'skipped beat', 'fluttering'],
            'swelling': ['swelling', 'edema', 'swollen', 'puffy'],
            'pale': ['pale', 'pallor', 'white skin'],
            'nausea': ['nausea', 'vomiting', 'sick to stomach'],
            'headache': ['headache', 'head hurts', 'migraine']
        }

    def extract_clinical_values(self, text):
        """Extract blood test values from text"""
        extracted = {}
        text = text.lower()
        
        for param, patterns in self.patterns.items():
            for pattern in patterns:
                match = re.search(pattern, text)
                if match:
                    value_str = match.group(1).replace(',', '')
                    try:
                        value = float(value_str)
                        extracted[param] = value
                        break  # Found a match for this parameter
                    except ValueError:
                        continue
                        
        return extracted

    def extract_symptoms(self, text):
        """Extract symptoms from text"""
        found_symptoms = []
        text = text.lower()
        
        for symptom_key, keywords in self.symptoms.items():
            for keyword in keywords:
                if keyword in text:
                    found_symptoms.append(symptom_key)
                    break
                    
        return found_symptoms
        
    def extract_demographics(self, text):
        """Extract basic demographics if present"""
        demographics = {}
        text = text.lower()
        
        # Age
        age_match = re.search(r'(\d+)\s*(?:years|yrs|yo)\s*old', text)
        if age_match:
            demographics['age'] = int(age_match.group(1))
            
        # Sex
        if 'male' in text and 'female' not in text:
            demographics['sex'] = 'Male'
        elif 'female' in text:
            demographics['sex'] = 'Female'
        elif ' man ' in text or ' boy ' in text:
            demographics['sex'] = 'Male'
        elif ' woman ' in text or ' girl ' in text:
            demographics['sex'] = 'Female'
            
        return demographics
