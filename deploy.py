import mlflow
import mlflow.pytorch
import os


model_name = os.getenv("MODEL_NAME")
model_version = os.getenv("MODEL_VERSION")

#Retrieve the model from MLflow Model Registry
model_uri = f"models:/{model_name}@{model_version}"  # Use the model version specified in the workflow input
model = mlflow.pytorch.load_model(model_uri)
# Save the model to a local directory
mlflow.pytorch.save_model(model, "model/")