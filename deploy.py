import mlflow
import mlflow.pytorch
import os

#Retrieve model version argument from workflow input
model_version = os.getenv("MODEL_VERSION")

#Retrieve the model from MLflow Model Registry
model_uri = f"models:/SimpleClassifier@{model_version}"  # Use the model version specified in the workflow input
model = mlflow.pytorch.load_model(model_uri)
# Save the model to a local directory
mlflow.pytorch.save_model(model, "model/")