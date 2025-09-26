import bentoml
import pickle


# Load the model from the downloaded pickle file
model_path = "model.pkl"  # Update the path if needed
with open(model_path, 'rb') as model_file:
    model = pickle.load(model_file)


# Save the model to BentoML with a unique name
bento_model = bentoml.sklearn.save_model("health_insurance_anomaly_detector", model)


print(f"Model registered with BentoML: {bento_model}")