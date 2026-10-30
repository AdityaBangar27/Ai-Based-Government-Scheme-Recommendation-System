import pandas as pd
import joblib
import json
import os
import sys

class SchemePredictor:
    """
    Load trained Random Forest model and make predictions
    """
    
    def __init__(self, models_path='../models'):
        # Support both current dir and ../models
        if os.path.exists(os.path.join(models_path, 'scheme_model.pkl')):
            self.models_path = models_path
        elif os.path.exists('scheme_model.pkl'):
            self.models_path = '.'
        elif os.path.exists(os.path.join(os.path.dirname(__file__), 'scheme_model.pkl')):
            self.models_path = os.path.dirname(__file__)
        else:
            self.models_path = os.path.join(os.path.dirname(__file__), '..', 'models')
            
        self.model = None
        self.encoders = {}
        self.feature_columns = None
        self.load_model()
    
    def load_model(self):
        """Load saved model and encoders"""
        try:
            model_path = os.path.join(self.models_path, 'scheme_model.pkl')
            encoders_path = os.path.join(self.models_path, 'encoders.pkl')
            config_path = os.path.join(self.models_path, 'model_config.json')
            
            if not os.path.exists(model_path):
                return False
            
            self.model = joblib.load(model_path)
            self.encoders = joblib.load(encoders_path)
            
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    self.feature_columns = config.get('feature_columns')
            
            return True
            
        except Exception:
            return False
    
    def predict(self, user_data):
        """
        Predict eligible schemes for a user with ML probability scores
        """
        try:
            if self.model is None and not self.load_model():
                return None
            
            # Standardize user features
            data = {
                'age': float(user_data.get('age', 25)),
                'income': float(user_data.get('income', user_data.get('annual_income', 100000))),
                'gender': str(user_data.get('gender', 'Male')),
                'occupation': str(user_data.get('occupation', 'General')),
                'education': str(user_data.get('education', 'Graduate')),
                'category': str(user_data.get('category', 'General')),
                'state': str(user_data.get('state', 'Maharashtra')),
                'disability_status': str(user_data.get('disability_status', 'No')),
                'farmer_status': str(user_data.get('farmer_status', 'No')),
                'student_status': str(user_data.get('student_status', 'No')),
                'employment_status': str(user_data.get('employment_status', 'Employed'))
            }
            
            input_df = pd.DataFrame([data])
            
            # Encode categorical features with fallback for unseen labels
            for col, encoder in self.encoders.items():
                if col != 'scheme_name' and col in input_df.columns:
                    val = str(input_df.at[0, col])
                    classes = list(encoder.classes_)
                    if val not in classes:
                        # Find case-insensitive or default to first class
                        matched = next((c for c in classes if c.lower() == val.lower()), classes[0])
                        input_df.at[0, col] = matched
                    input_df[col] = encoder.transform(input_df[col].astype(str))
            
            # Select feature columns
            if self.feature_columns:
                for col in self.feature_columns:
                    if col not in input_df.columns:
                        input_df[col] = 0
                input_df = input_df[self.feature_columns]
            
            # Get predictions with probabilities
            if hasattr(self.model, 'predict_proba'):
                probabilities = self.model.predict_proba(input_df)[0]
                scheme_names = self.encoders['scheme_name'].classes_
                
                predictions = []
                for scheme, prob in zip(scheme_names, probabilities):
                    score = float(prob) * 100
                    predictions.append({
                        'scheme_name': scheme,
                        'ml_score': round(score, 1),
                        'recommendation_score': round(min(98.5, max(60.0, score * 1.5 + 50.0)), 1)
                    })
                
                # Sort descending
                predictions.sort(key=lambda x: x['recommendation_score'], reverse=True)
                return predictions
            
            return None
        except Exception as e:
            return None

# CLI Execution Support
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] != 'run':
        try:
            raw_input = sys.argv[1]
            user_data = json.loads(raw_input)
            predictor = SchemePredictor()
            results = predictor.predict(user_data)
            print(json.dumps(results or []))
            sys.exit(0)
        except Exception as e:
            print(json.dumps([]))
            sys.exit(0)
    else:
        # Flask API endpoint wrapper
        try:
            from flask import Flask, request, jsonify
            app = Flask(__name__)
            predictor = SchemePredictor()

            @app.route('/predict', methods=['POST'])
            def predict_api():
                user_data = request.json or {}
                predictions = predictor.predict(user_data)
                return jsonify({
                    'status': 'success',
                    'recommendations': predictions or []
                })

            app.run(port=5001, debug=False)
        except Exception:
            pass
