"""
Prevention Advisor
Provides disease-specific prevention and management advice.
"""

class PreventionAdvisor:
    def __init__(self):
        self.advice_db = {
            'Diabetes': {
                'description': "A metabolic disorder characterized by high blood sugar levels.",
                'immediate_actions': [
                    "Monitor blood glucose levels daily",
                    "Consult an endocrinologist"
                ],
                'lifestyle': [
                    "Adopt a low-glycemic index diet",
                    "Engage in regular physical activity (150 mins/week)",
                    "Maintain a healthy weight"
                ],
                'diet': [
                    "Reduce intake of sugary drinks and refined carbs",
                    "Increase fiber intake (vegetables, whole grains)",
                    "Control portion sizes"
                ]
            },
            'Heart Di': {
                'description': "Conditions affecting the heart structure and function.",
                'immediate_actions': [
                    "Consult a cardiologist immediately",
                    "Monitor blood pressure daily"
                ],
                'lifestyle': [
                    "Quit smoking if applicable",
                    "Manage stress levels",
                    "Aim for 30 minutes of moderate exercise daily"
                ],
                'diet': [
                    "Adopt a Mediterranean-style diet",
                    "Limit sodium intake (<2300mg/day)",
                    "Reduce saturated and trans fats"
                ]
            },
            'Anemia': {
                'description': "A condition where you lack enough healthy red blood cells to carry adequate oxygen.",
                'immediate_actions': [
                    "Consult a doctor for blood work",
                    "Check for underlying causes"
                ],
                'lifestyle': [
                    "Ensure adequate rest",
                    "Avoid tea/coffee with meals (inhibits iron absorption)"
                ],
                'diet': [
                    "Increase iron-rich foods (spinach, red meat, lentils)",
                    "Consume Vitamin C to enhance iron absorption",
                    "Consider iron supplements if prescribed"
                ]
            },
            'Thalasse': {
                'description': "An inherited blood disorder affecting hemoglobin production.",
                'immediate_actions': [
                    "Genetic counseling",
                    "Regular hematologist check-ups"
                ],
                'lifestyle': [
                    "Avoid iron supplements unless prescribed (risk of overload)",
                    "Protect against infections"
                ],
                'diet': [
                    "Drink tea with meals to reduce iron absorption",
                    "Ensure adequate folate intake"
                ]
            },
            'Thromboc': {
                'description': "A condition characterized by low platelet count.",
                'immediate_actions': [
                    "Avoid activities with risk of injury/bleeding",
                    "Review medications with doctor"
                ],
                'lifestyle': [
                    "Use soft toothbrush",
                    "Avoid alcohol (can slow platelet production)"
                ],
                'diet': [
                    "Eat plenty of leafy greens",
                    "Avoid quinine-containing foods (tonic water)"
                ]
            },
            'Healthy': {
                'description': "Your parameters appear to be within normal ranges.",
                'immediate_actions': [
                    "Continue regular check-ups"
                ],
                'lifestyle': [
                    "Maintain current healthy habits",
                    "Stay hydrated",
                    "Get 7-9 hours of sleep"
                ],
                'diet': [
                    "Balanced diet with variety of nutrients",
                    "Limit processed foods"
                ]
            }
        }

    def get_advice(self, disease):
        """Get prevention advice for a specific disease"""
        # Handle potential key mismatches
        if disease not in self.advice_db:
            # Try partial match
            for key in self.advice_db:
                if key in disease or disease in key:
                    return self.advice_db[key]
            return self.advice_db['Healthy'] # Fallback
            
        return self.advice_db[disease]
