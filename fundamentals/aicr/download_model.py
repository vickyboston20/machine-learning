import mlflow
import shutil
import os

# Set the MLflow tracking URI to your server's address
mlflow.set_tracking_uri("http://localhost:5000")  # Replace <your-server-ip> with your server's IP or hostname

# Define the MLflow artifact URI
# Note: Replace the artifact_uri with the actual path to the model artifact in your MLflow UI
artifact_uri = "mlflow-artifacts:/818279823369072980/models/m-e8ba07fdec0c4114a85370d61bf39b69/artifacts/model.pkl"

# Specify the local path to save the downloaded file
local_path = "model.pkl"

# Download the artifact
artifact_path = mlflow.artifacts.download_artifacts(artifact_uri=artifact_uri)
print(artifact_path)

# Move the file to the desired location
if os.path.exists(local_path):
    os.remove(local_path)
# If the file already exists, remove it
shutil.move(artifact_path, local_path)

print(f"Model downloaded and saved to: {local_path}")