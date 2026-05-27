from core import CatsAndDogsDataset, SimpleClassifier, train_model, test_model
from torch.utils.data import DataLoader
from loader import DATA_BUCKET_NAME, load_data_from_s3

import os
import mlflow
import mlflow.pytorch
import torch.nn as nn
import torch.optim as optim

if __name__ == "__main__":
    
    data_dir = 'data'
    data_prefix = 'cats-and-dogs-image-classification/'
    input_size = 64 * 64 * 3  
    hidden_size = 125
    output_size = 2  # 2 classes: cat and dog
    epochs = 10

    experiment_name = os.getenv("MLFLOW_EXPERIMENT_NAME")
    if not experiment_name:
        raise ValueError("MLFLOW_EXPERIMENT_NAME environment variable is not set. Please set it to the name of your MLflow experiment.")

    if not DATA_BUCKET_NAME:
        raise ValueError("DATA_BUCKET_NAME environment variable is not set. Please set it to the name of your S3 bucket containing the data.")

    # Download data from S3 (if needed)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        load_data_from_s3(bucket_name=DATA_BUCKET_NAME, prefix=data_prefix, local_path=data_dir)
    else:
        print(f"Data directory '{data_dir}' already exists. Skipping download.")

    mlflow.set_experiment(experiment_name)
           
    with mlflow.start_run():
        model = SimpleClassifier(input_size, hidden_size, output_size)
        optimizer = optim.SGD(model.parameters(), lr=0.01)
        criterion = nn.NLLLoss()

        # Loading datasets
        train_dataset = CatsAndDogsDataset(data_dir, target_size=(64, 64), color_mode='RGB', train=True)
        train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

        test_dataset = CatsAndDogsDataset(data_dir, target_size=(64, 64), color_mode='RGB', train=False)
        test_loader = DataLoader(test_dataset, batch_size=32, shuffle=True)

        loss_history = []  # Initialize loss history list
        train_model(model, input_size, train_loader, optimizer, criterion, epochs, loss_history=loss_history)

        print("Loss:", loss_history)

        # Evaluate the model on the test dataset
        asset_accuracy = test_model(model, input_size, test_loader)
        print(asset_accuracy)

        mlflow.log_metric("accuracy", asset_accuracy)  # Log accuracy to MLflow
        mlflow.pytorch.log_model(model, "simple_classifier")  # Log the model to MLflow
