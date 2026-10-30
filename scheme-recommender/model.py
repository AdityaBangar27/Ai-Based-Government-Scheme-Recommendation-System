import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Load Datasets
users = pd.read_csv("users.csv")
schemes = pd.read_csv("schemes.csv")

# User Data Cleaning

print("Missing values before cleaning:")
print(users.isnull().sum())

# Remove missing values
users = users.dropna()

# Remove duplicates
users = users.drop_duplicates()

# Strip spaces from text columns
users = users.apply(lambda col: col.str.strip() if col.dtype == "object" else col)

# Convert text to lowercase
users = users.apply(lambda col: col.str.lower() if col.dtype == "object" else col)

print("\nCleaned Users Data:")
print(users.head())

# Scheme Data Cleaning + Conversion

# Replace "No Limit"
schemes['Income_Limit'] = schemes['Income_Limit'].replace('No Limit', 999999999)

# Convert numeric columns
schemes['Income_Limit'] = pd.to_numeric(schemes['Income_Limit'])
schemes['Min_Age'] = pd.to_numeric(schemes['Min_Age'])
schemes['Max_Age'] = pd.to_numeric(schemes['Max_Age'])

users['Age'] = pd.to_numeric(users['Age'])
users['Income'] = pd.to_numeric(users['Income'])

# Create Matching Dataset

data = []

for _, user in users.iterrows():
    for _, scheme in schemes.iterrows():

        if (
            user['Age'] >= scheme['Min_Age'] and
            user['Age'] <= scheme['Max_Age'] and
            user['Income'] <= scheme['Income_Limit']
        ):
            data.append([
                user['Age'],
                user['Gender'],
                user['Income'],
                user['State'],
                user['Occupation'],
                scheme['Scheme_Name']
            ])


# Final DataFrame (FIXED)

df = pd.DataFrame(data, columns=[
    'Age', 'Gender', 'Income', 'State', 'Occupation', 'Scheme_Name'
])

print(df.head())


# Label Encoding

le_gender = LabelEncoder()
df['Gender'] = le_gender.fit_transform(df['Gender'])

le_state = LabelEncoder()
df['State'] = le_state.fit_transform(df['State'])

le_occ = LabelEncoder()
df['Occupation'] = le_occ.fit_transform(df['Occupation'])

le_scheme = LabelEncoder()
df['Scheme_Name'] = le_scheme.fit_transform(df['Scheme_Name'])

print("\nEncoded Data:")
print(df.head())

# Use the cleaned `users` dataset for modeling
# Step 1: Prepare features (X) and target (y)
df = users.copy()

# Ensure target exists
if 'Recommended_Scheme' not in df.columns:
    raise KeyError('Recommended_Scheme column missing from users.csv')

X = df.drop('Recommended_Scheme', axis=1)
y = df['Recommended_Scheme']

# Step 2: Encode categorical features using LabelEncoder and save encoders
from sklearn.preprocessing import LabelEncoder
encoders = {}
categorical_cols = X.select_dtypes(include=['object', 'category']).columns.tolist()
for col in categorical_cols:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col])
    encoders[col] = le

print("\nFeature columns after encoding:")
print(X.head())

# Step 3: Train-test split
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Step 4: Train Random Forest classifier
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(random_state=42, n_estimators=100)
model.fit(X_train, y_train)

# Step 5: Evaluate model accuracy on test set
from sklearn.metrics import accuracy_score
y_pred = model.predict(X_test)
print('\nAccuracy:', accuracy_score(y_test, y_pred))

# Step 6: Test with a new user example.
# Create a valid example by taking first row's categorical values and changing Age/Income
example_raw = X.drop(columns=categorical_cols).iloc[0].to_dict() if len(categorical_cols) > 0 else X.iloc[0].to_dict()
# Update numeric fields for the test sample
example_raw['Age'] = 22
if 'Income' in example_raw:
    example_raw['Income'] = 20000

# For categorical columns, use the first user's original (unencoded) values from `users`
example = {}
for col in X.columns:
    if col in categorical_cols:
        # find original value from users to ensure encoder can transform
        example[col] = users.iloc[0][col]
    else:
        example[col] = example_raw.get(col, X.iloc[0][col])

example_df = pd.DataFrame([example])
# Encode categorical columns in the example using the fitted encoders
for col, le in encoders.items():
    example_df[col] = le.transform(example_df[col])

print('\nExample input (encoded) for prediction:')
print(example_df)

predicted_scheme = model.predict(example_df)
print('\nPredicted scheme for example user:', predicted_scheme)

# Step 7: Save trained model and encoders for later use
import joblib
joblib.dump(model, 'scheme_model.pkl')
joblib.dump(encoders, 'encoders.pkl')
print('\nSaved model to scheme_model.pkl and encoders to encoders.pkl')