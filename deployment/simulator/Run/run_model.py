import xgboost as xgb
import pandas as pd
import numpy as np
import json5  

# Path to the pre-trained XGBoost model (JSON format)
# IMPORTANT: Ensure this path points to your specific model file
MODEL_PATH = "xgboost_model_default.json"

# Load the saved XGBoost model
best_model = xgb.Booster()
best_model.load_model(MODEL_PATH)

# Feature names in the exact order used during model training
# DO NOT MODIFY this list unless you know exactly what you're doing
expected_features = [
    'num__Data size sum (MB)',
    'num__Number of rows sum',
    'num__Number of columns sum',
    'num__maxStreams',
    'num__RAM (GB)',
    'num__CPU',
    'num__Disk (GB)',
    'num__External Disk (GB)',
    'cat__compress_GZIP',
    'cat__compress_LZ4',
    'cat__compress_NO',
    'cat__binary_False',
    'cat__binary_True'
]

def prepare_categorical_input(categorical_features):
    """
    Convert user-friendly categorical inputs to one-hot encoded format
    
    Args:
    categorical_features (dict): A dictionary of categorical feature inputs
    
    Returns:
    dict: One-hot encoded categorical features
    """
    # Initialize all categorical features to 0
    cat_input = {
        'cat__compress_GZIP': 0,
        'cat__compress_LZ4': 0,
        'cat__compress_NO': 0,
        'cat__binary_False': 0,
        'cat__binary_True': 0
    }
    
    # Handle compression type
    if 'compress' in categorical_features:
        # Allowed compression types: 'GZIP', 'LZ4', 'NO'
        compress_mapping = {
            'GZIP': 'cat__compress_GZIP',
            'LZ4': 'cat__compress_LZ4',
            'NO': 'cat__compress_NO'
        }
        compress_key = compress_mapping.get(categorical_features['compress'].upper())
        if compress_key:
            cat_input[compress_key] = 1
        else:
            print(f"Warning: Invalid compression type '{categorical_features['compress']}'. Using default.")
    
    # Handle binary feature
    if 'binary' in categorical_features:
        # Allowed binary types: True, False
        binary_mapping = {
            'False': 'cat__binary_False',
            'True': 'cat__binary_True'
        }
        binary_key = binary_mapping.get(str(categorical_features['binary']).capitalize())
        if binary_key:
            cat_input[binary_key] = 1
        else:
            print(f"Warning: Invalid binary type '{categorical_features['binary']}'. Using default.")
    
    return cat_input

def predict_performance(numeric_features, categorical_features):
    """
    Predict performance based on numeric and categorical inputs
    
    Args:
    numeric_features (dict): Numeric feature inputs
    categorical_features (dict): Categorical feature inputs
    
    Returns:
    float: Predicted performance
    """
    # Prepare categorical inputs
    cat_input = prepare_categorical_input(categorical_features)
    
    # Combine numeric and categorical inputs
    sample_input = {**numeric_features, **cat_input}
    
    # Ensure the input follows the exact feature order
    input_df = pd.DataFrame([sample_input])
    input_df = input_df[expected_features]
    
    # Convert to DMatrix and predict
    dtest = xgb.DMatrix(input_df)
    predictions = best_model.predict(dtest)
    
    return predictions[0]

# MAIN EXECUTION SECTION
# =====================
# Users should modify the values in this section to match their specific use case

if __name__ == "__main__":
    
    config_path = "configs/config.jsonc"
    with open(config_path, "r") as file:
        config = json5.load(file)

    numeric_input = config["numeric_input"]
    categorical_input = config["categorical_input"]

    # Run prediction
    prediction = predict_performance(numeric_input, categorical_input)
    
    # Print detailed results
    print("\n=== Data Migration Performance Prediction ===")
    print("Numeric Input:")
    for feature, value in numeric_input.items():
        print(f"{feature}: {value}")
    
    print("\nCategorical Input:")
    for feature, value in categorical_input.items():
        print(f"{feature}: {value}")
    
    print(f"\nPredicted Data Migration Performance: {prediction / 60} (minutes)")