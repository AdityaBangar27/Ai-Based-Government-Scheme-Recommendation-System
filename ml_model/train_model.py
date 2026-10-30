import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib
import json
import os

class SchemeRecommender:
    """
    AI-Powered Government Scheme Recommendation Engine using Random Forest
    """
    
    def __init__(self, datasets_path='../datasets', models_path='../models'):
        self.datasets_path = datasets_path
        self.models_path = models_path
        self.model = None
        self.encoders = {}
        self.feature_columns = None
        
    def load_data(self):
        """Load and prepare training data"""
        try:
            # Load datasets
            users = pd.read_csv(os.path.join(self.datasets_path, 'users.csv'))
            schemes = pd.read_csv(os.path.join(self.datasets_path, 'schemes.csv'))
            
            print("✓ Data loaded successfully")
            print(f"  Users: {len(users)} records")
            print(f"  Schemes: {len(schemes)} records")
            
            return users, schemes
        except Exception as e:
            print(f"✗ Error loading data: {e}")
            return None, None
    
    def prepare_features(self, users, schemes):
        """Prepare features for ML model"""
        try:
            # Create matching dataset
            data = []
            
            if len(users) == 0:
                print("[*] No user records found in users.csv. Generating synthetic training profiles...")
                import random
                occupations = ['Farmer', 'Student', 'Artisan', 'Unorganized Worker', 'Self-Employed', 'Unemployed', 'Teacher', 'Labourer']
                educations = ['10th Pass', '12th Pass', 'Graduate', 'Post Graduate', 'Illiterate']
                categories = ['General', 'OBC', 'SC', 'ST', 'EWS']
                states = ['Maharashtra', 'Delhi', 'Uttar Pradesh', 'Gujarat', 'Karnataka', 'Bihar', 'Rajasthan', 'Punjab']
                genders = ['Male', 'Female']
                
                synthetic_users = []
                for i in range(200):
                    occ = random.choice(occupations)
                    age = random.randint(6, 75)
                    income = random.randint(20000, 800000)
                    synthetic_users.append({
                        'user_id': str(1000 + i),
                        'age': age,
                        'annual_income': income,
                        'gender': random.choice(genders),
                        'occupation': occ,
                        'education': random.choice(educations),
                        'category': random.choice(categories),
                        'state': random.choice(states),
                        'disability_status': 'Yes' if random.random() < 0.1 else 'No',
                        'farmer_status': 'Yes' if occ == 'Farmer' or random.random() < 0.2 else 'No',
                        'student_status': 'Yes' if occ == 'Student' or (age <= 25 and random.random() < 0.5) else 'No',
                        'employment_status': 'Unemployed' if occ == 'Unemployed' else 'Employed'
                    })
                users = pd.DataFrame(synthetic_users)
                print(f"[*] Generated {len(users)} synthetic training profiles.")

            for _, user in users.iterrows():
                for _, scheme in schemes.iterrows():
                    # Check eligibility
                    if pd.isna(user['age']) or pd.isna(scheme['min_age']):
                        continue
                    
                    try:
                        age = float(user['age'])
                        min_age = float(scheme['min_age'])
                        max_age = float(scheme['max_age'])
                        income = float(user['annual_income']) if not pd.isna(user['annual_income']) else 0
                        raw_limit = str(scheme['income_limit']).strip().lower()
                        if raw_limit in ['unlimited', 'nan', 'none', '']:
                            income_limit = 999999999.0
                        else:
                            income_limit = float(scheme['income_limit'])
                    except (ValueError, TypeError):
                        income_limit = 999999999.0
                    
                    if (age >= min_age and age <= max_age and income <= income_limit):
                        data.append({
                            'age': age,
                            'income': income,
                            'gender': user['gender'] if not pd.isna(user['gender']) else 'Not Specified',
                            'occupation': user['occupation'] if not pd.isna(user['occupation']) else 'General',
                            'education': user['education'] if not pd.isna(user['education']) else 'Not Specified',
                            'category': user['category'] if not pd.isna(user['category']) else 'General',
                            'state': user['state'] if not pd.isna(user['state']) else 'Not Specified',
                            'disability_status': user['disability_status'] if not pd.isna(user['disability_status']) else 'No',
                            'farmer_status': user['farmer_status'] if not pd.isna(user['farmer_status']) else 'No',
                            'student_status': user['student_status'] if not pd.isna(user['student_status']) else 'No',
                            'employment_status': user['employment_status'] if not pd.isna(user['employment_status']) else 'Not Employed',
                            'scheme_id': scheme['scheme_id'],
                            'scheme_name': scheme['scheme_name']
                        })
            
            df = pd.DataFrame(data)
            print(f"[OK] Training dataset prepared: {len(df)} eligible user-scheme pairs")
            return df
            
        except Exception as e:
            print(f"✗ Error preparing features: {e}")
            return None
    
    def encode_features(self, df):
        """Encode categorical features"""
        try:
            X = df.drop(['scheme_id', 'scheme_name'], axis=1)
            y = df['scheme_name']
            
            # Store feature columns
            self.feature_columns = X.columns.tolist()
            
            # Encode categorical columns
            categorical_cols = ['gender', 'occupation', 'education', 'category', 'state', 
                              'disability_status', 'farmer_status', 'student_status', 'employment_status']
            
            for col in categorical_cols:
                if col in X.columns:
                    le = LabelEncoder()
                    X[col] = le.fit_transform(X[col].astype(str))
                    self.encoders[col] = le
            
            # Encode target
            le_scheme = LabelEncoder()
            y_encoded = le_scheme.fit_transform(y)
            self.encoders['scheme_name'] = le_scheme
            
            print(f"✓ Features encoded: {len(X.columns)} features, {len(y_encoded)} samples")
            return X, y_encoded
            
        except Exception as e:
            print(f"✗ Error encoding features: {e}")
            return None, None
    
    def train_model(self, X, y):
        """Train Random Forest Classifier"""
        try:
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            print(f"✓ Train/Test split: {len(X_train)} train, {len(X_test)} test")
            
            # Train Random Forest
            self.model = RandomForestClassifier(
                n_estimators=100,
                max_depth=15,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1
            )
            
            self.model.fit(X_train, y_train)
            print("✓ Random Forest model trained (100 trees)")
            
            # Evaluate
            train_pred = self.model.predict(X_train)
            test_pred = self.model.predict(X_test)
            
            train_acc = accuracy_score(y_train, train_pred)
            test_acc = accuracy_score(y_test, test_pred)
            precision = precision_score(y_test, test_pred, average='weighted', zero_division=0)
            recall = recall_score(y_test, test_pred, average='weighted', zero_division=0)
            f1 = f1_score(y_test, test_pred, average='weighted', zero_division=0)
            
            metrics = {
                'train_accuracy': float(train_acc),
                'test_accuracy': float(test_acc),
                'precision': float(precision),
                'recall': float(recall),
                'f1_score': float(f1)
            }
            
            print("\n📊 Model Performance:")
            print(f"   Train Accuracy: {train_acc:.4f}")
            print(f"   Test Accuracy: {test_acc:.4f}")
            print(f"   Precision: {precision:.4f}")
            print(f"   Recall: {recall:.4f}")
            print(f"   F1 Score: {f1:.4f}")
            
            return metrics
            
        except Exception as e:
            print(f"✗ Error training model: {e}")
            return None
    
    def save_model(self):
        """Save model and encoders"""
        try:
            for target_dir in [self.models_path, '.']:
                os.makedirs(target_dir, exist_ok=True)
                model_path = os.path.join(target_dir, 'scheme_model.pkl')
                encoders_path = os.path.join(target_dir, 'encoders.pkl')
                config_path = os.path.join(target_dir, 'model_config.json')
                
                joblib.dump(self.model, model_path)
                joblib.dump(self.encoders, encoders_path)
                
                config = {
                    'feature_columns': self.feature_columns,
                    'n_estimators': 100,
                    'model_type': 'RandomForestClassifier'
                }
                
                with open(config_path, 'w') as f:
                    json.dump(config, f, indent=4)
                
                print(f"[OK] Saved artifacts to {target_dir}")
            
        except Exception as e:
            print(f"[!] Error saving model: {e}")
    
    def predict(self, user_data):
        """Predict eligible schemes for a user"""
        try:
            if self.model is None:
                print("✗ Model not loaded")
                return None
            
            # Prepare input
            input_df = pd.DataFrame([user_data])
            
            # Encode features
            for col in self.encoders:
                if col != 'scheme_name' and col in input_df.columns:
                    input_df[col] = self.encoders[col].transform(input_df[col].astype(str))
            
            # Select only feature columns used during training
            input_df = input_df[self.feature_columns]
            
            # Get probabilities for all schemes
            if hasattr(self.model, 'predict_proba'):
                probabilities = self.model.predict_proba(input_df)[0]
                scheme_names = self.encoders['scheme_name'].classes_
                
                predictions = []
                for scheme, prob in zip(scheme_names, probabilities):
                    predictions.append({
                        'scheme': scheme,
                        'eligibility_score': float(prob) * 100
                    })
                
                # Sort by eligibility score
                predictions.sort(key=lambda x: x['eligibility_score'], reverse=True)
                return predictions[:10]  # Top 10 schemes
            
        except Exception as e:
            print(f"✗ Error during prediction: {e}")
            return None
    
    def train_full_pipeline(self):
        """Complete training pipeline"""
        print("\n🚀 Starting Scheme Recommender Training Pipeline\n")
        
        users, schemes = self.load_data()
        if users is None or schemes is None:
            return
        
        df = self.prepare_features(users, schemes)
        if df is None or len(df) == 0:
            print("✗ No training data available")
            return
        
        X, y = self.encode_features(df)
        if X is None:
            return
        
        metrics = self.train_model(X, y)
        if metrics is None:
            return
        
        self.save_model()
        
        print("\n✅ Training pipeline completed successfully!\n")
        return metrics


if __name__ == '__main__':
    recommender = SchemeRecommender()
    recommender.train_full_pipeline()
    
    # Example prediction
    example_user = {
        'age': 35,
        'income': 400000,
        'gender': 'male',
        'occupation': 'farmer',
        'education': 'graduate',
        'category': 'general',
        'state': 'maharashtra',
        'disability_status': 'no',
        'farmer_status': 'yes',
        'student_status': 'no',
        'employment_status': 'self-employed'
    }
    
    recommendations = recommender.predict(example_user)
    if recommendations:
        print("\n🎯 Recommendations for example user:")
        for i, rec in enumerate(recommendations, 1):
            print(f"   {i}. {rec['scheme']} - {rec['eligibility_score']:.1f}%")
