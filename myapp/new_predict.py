import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

# Assuming 'crop_yield.csv' is in the current directory. Adjust the path as necessary.
def predict_crop(area,season,state,rainfall):
    df = pd.read_csv(r'E:\VINEETH\Crop_Recommendation\Crop_recommendation\myapp\crop_yield.csv')

    # Print dataset columns for inspection
    print("Dataset columns:", df.columns.tolist())

    # Encode categorical variables
    label_encoders = {}
    categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
    for column in categorical_columns:
        le = LabelEncoder()
        df[column] = le.fit_transform(df[column])
        label_encoders[column] = le

    # Define features and target based on your dataset structure
    features = ['area', 'Annual_Rainfall', 'season', 'State']  # Including 'State' as a feature
    target = 'Crop'

    # Split the dataset into training and testing sets
    X = df[features]
    y = df[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize and train the model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy}")

    # Function to recommend a crop based on area, annual rainfall, season, and state
    def recommend_crop(area, annual_rainfall, season, state):
        # Validate and encode inputs
        try:
            season_encoded = label_encoders['season'].transform([season])[0]
            state_encoded = label_encoders['State'].transform([state])[0]
        except ValueError as e:
            # Handling unknown or invalid inputs
            print(f"Input error: {e}")
            return "Invalid input provided. Please check your season and state values."

        # Creating a DataFrame for the input features
        inputs = pd.DataFrame([[area, annual_rainfall, season_encoded, state_encoded]], columns=features)
        # Predicting the crop
        recommended_crop_index = model.predict(inputs)[0]
        recommended_crop = label_encoders['Crop'].inverse_transform([recommended_crop_index])
        return recommended_crop[0]

    # Example inputs from the user
    example_area = area
    example_annual_rainfall = rainfall
    example_season = season  # Example must match the encoded classes
    example_state = state  # Example must match the encoded classes

    # Display encoded classes for 'season' and 'State' to help with input adjustments
    print("Season encoded classes:", label_encoders['season'].classes_)
    print("State encoded classes:", label_encoders['State'].classes_)

    # Predicting and printing the recommended crop based on example inputs
    recommended_crop = recommend_crop(example_area, example_annual_rainfall, example_season, example_state)
    print(f"Recommended Crop: {recommended_crop}")
    return recommended_crop

# area=int(input("area : "))
# rainfall=int(input("rainfall : "))
# season=input("ENter the season :")
# state=input("ENter the state :")

# predict_crop(area,season,state,rainfall)