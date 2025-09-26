import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
import mlflow
import mlflow.sklearn


# Load the synthetic data
df = pd.read_csv('synthetic_health_claims.csv')


# Set the MLflow tracking URI
mlflow.set_tracking_uri("http://127.0.0.1:5000")


# Define the features for the model. Note that 'claim_id' is not used.
features = ['claim_amount', 'num_services', 'patient_age', 'provider_id', 'days_since_last_claim']


# Split the data into training and test sets
X_train, X_test = train_test_split(df[features], test_size=0.2, random_state=42)


# Create (or set) the experiment in MLflow
mlflow.set_experiment("Health Insurance Claim Anomaly Detection")


with mlflow.start_run():
    # Train the Isolation Forest model
    model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
    model.fit(X_train)


    # Predict anomalies on training and test sets
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)


    # Calculate the percentage of detected anomalies
    train_anomaly_percentage = (y_pred_train == -1).mean() * 100
    test_anomaly_percentage = (y_pred_test == -1).mean() * 100


    # Log model parameters
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("contamination", 0.05)


    # Log computed metrics
    mlflow.log_metric("train_anomaly_percentage", train_anomaly_percentage)
    mlflow.log_metric("test_anomaly_percentage", test_anomaly_percentage)


    # Log the model artifact to MLflow
    mlflow.sklearn.log_model(model, "model")


    print(f"Train Anomaly Percentage: {train_anomaly_percentage:.2f}%")
    print(f"Test Anomaly Percentage: {test_anomaly_percentage:.2f}%")
    print("Model and metrics logged to MLflow.")