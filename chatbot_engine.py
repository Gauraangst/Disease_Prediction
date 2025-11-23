"""
Chatbot Engine
Orchestrates the medical chatbot conversation, integrating NLP, mapping, estimation, and ML prediction.
"""
import joblib
import numpy as np
import pandas as pd
from medical_nlp import MedicalNLPExtractor
from symptom_mapper import SymptomMapper
from param_estimator import ParameterEstimator
from prevention_advisor import PreventionAdvisor
from module_b_scaling_bridge import ScalingBridge

class MedicalChatbot:
    def __init__(self, model_path='models/best_model.pkl', 
                 scaler_path='models/scaling_bridge.pkl',
                 label_encoder_path='models/label_encoder.pkl',
                 feature_names_path='models/feature_names.pkl'):
        
        # Initialize components
        self.nlp = MedicalNLPExtractor()
        self.mapper = SymptomMapper()
        self.estimator = ParameterEstimator()
        self.advisor = PreventionAdvisor()
        
        # Load ML models
        try:
            self.model = joblib.load(model_path)
            self.scaling_bridge = ScalingBridge.load(scaler_path)
            self.label_encoder = joblib.load(label_encoder_path)
            self.feature_names = joblib.load(feature_names_path)
            self.model_loaded = True
        except Exception as e:
            print(f"Error loading models: {e}")
            self.model_loaded = False

    def process_message(self, user_input, session_context=None):
        """
        Process a user message and generate a response.
        
        Args:
            user_input (str): The user's natural language message
            session_context (dict): Previous context (optional)
            
        Returns:
            dict: Response containing text, extracted data, and prediction (if applicable)
        """
        if session_context is None:
            session_context = {}
            
        # 1. Extract information
        extracted_values = self.nlp.extract_clinical_values(user_input)
        symptoms = self.nlp.extract_symptoms(user_input)
        demographics = self.nlp.extract_demographics(user_input)
        
        # Merge with existing context
        current_values = session_context.get('values', {})
        current_values.update(extracted_values)
        
        current_symptoms = session_context.get('symptoms', [])
        current_symptoms.extend([s for s in symptoms if s not in current_symptoms])
        
        # Debug logging
        print(f"DEBUG: User Input: {user_input}")
        print(f"DEBUG: Extracted Values: {extracted_values}")
        print(f"DEBUG: Extracted Symptoms: {symptoms}")
        print(f"DEBUG: Current Context Values: {current_values}")
        print(f"DEBUG: Current Context Symptoms: {current_symptoms}")
        
        # 2. Determine if we have enough info to predict
        # Relaxed threshold: Predict if we have ANY meaningful input (1 value or 1 symptom)
        # The estimator will handle the rest
        should_predict = (len(current_values) + len(current_symptoms)) >= 1
        
        response = {
            'text': "",
            'context': {
                'values': current_values,
                'symptoms': current_symptoms,
                'demographics': demographics
            },
            'prediction': None
        }
        
        if not should_predict:
            response['text'] = (
                "I've noted your input. To give you an accurate assessment, could you provide more details? "
                "For example, do you have any recent blood test results (like Glucose, Cholesterol, or Hemoglobin) "
                "or are you experiencing other symptoms?"
            )
            return response
            
        # 3. Prepare for prediction
        if not self.model_loaded:
            response['text'] = "I'm sorry, but my medical knowledge base is currently unavailable. Please try again later."
            return response
            
        # Get implied parameters from symptoms
        implied_params = self.mapper.get_implied_parameters(current_symptoms)
        
        # Estimate missing values
        full_features = self.estimator.estimate_missing_values(
            current_values, implied_params, demographics
        )
        
        # Calculate derived features (same as in app.py)
        epsilon = 1e-6
        full_features['LDL_HDL_Ratio'] = full_features['LDL Cholesterol'] / (full_features['HDL Cholesterol'] + epsilon)
        full_features['Chol_HDL_Ratio'] = full_features['Cholesterol'] / (full_features['HDL Cholesterol'] + epsilon)
        full_features['Glucose_Insulin_Interaction'] = full_features['Glucose'] * full_features['Insulin']
        full_features['MAP'] = full_features['Diastolic Blood Pressure'] + (1/3 * (full_features['Systolic Blood Pressure'] - full_features['Diastolic Blood Pressure']))
        
        # 4. Make Prediction
        try:
            # Scale features
            scaled_features = self.scaling_bridge.scale_to_array(full_features, self.feature_names)
            
            # Predict
            prediction_idx = self.model.predict(scaled_features.reshape(1, -1))[0]
            prediction = self.label_encoder.inverse_transform([prediction_idx])[0]
            probabilities = self.model.predict_proba(scaled_features.reshape(1, -1))[0]
            confidence = max(probabilities) * 100
            
            # --- CARDIAC OVERRIDE CHECK (Safety) ---
            cardiac_risk_score = 0
            if full_features.get('Troponin', 0) > 0.04: cardiac_risk_score += 40
            if full_features.get('C-reactive Protein', 0) > 3.0: cardiac_risk_score += 20
            if full_features.get('LDL Cholesterol', 0) > 160: cardiac_risk_score += 15
            if full_features.get('Systolic Blood Pressure', 0) > 140: cardiac_risk_score += 15
            
            if cardiac_risk_score >= 60 and prediction != 'Heart Di':
                prediction = 'Heart Di'
                confidence = 95.0
                response['cardiac_override'] = True
            # ---------------------------------------
            
            # Get advice
            advice = self.advisor.get_advice(prediction)
            
            # Construct response text
            symptom_str = ", ".join(current_symptoms) if current_symptoms else "reported symptoms"
            
            response_text = f"Based on your {symptom_str} and the clinical values provided (or estimated), "
            response_text += f"my assessment points to **{prediction}** (Confidence: {confidence:.1f}%).\n\n"
            
            response_text += f"**Analysis:**\n{advice['description']}\n\n"
            
            response_text += "**Key Indicators:**\n"
            # List abnormal values
            for param, val in current_values.items():
                response_text += f"- {param}: {val}\n"
            if implied_params:
                response_text += f"- (Inferred from symptoms: {', '.join(implied_params.keys())})\n"
                
            response_text += "\n**Recommended Actions:**\n"
            for action in advice['immediate_actions']:
                response_text += f"- {action}\n"
                
            response_text += "\n**Prevention & Lifestyle:**\n"
            for tip in advice['lifestyle']:
                response_text += f"- {tip}\n"
                
            response['text'] = response_text
            response['prediction'] = {
                'disease': prediction,
                'confidence': confidence,
                'advice': advice
            }
            
        except Exception as e:
            print(f"Prediction error: {e}")
            response['text'] = "I encountered an error while analyzing your data. Please ensure you've provided valid clinical values."
            
        return response
