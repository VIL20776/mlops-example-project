from utils import CatsAndDogsDataset, SimpleClassifier, train_model, test_model
from torch.utils.data import DataLoader


import mlflow
import mlflow.pytorch
import torch
import torch.nn as nn
import torch.optim as optim

if __name__ == "__main__":
    data_dir = 'data'
    input_size = 64 * 64 * 3  
    hidden_size = 125
    output_size = 2  # 2 classes: cat and dog
    epochs = 5

    # mlflow.set_tracking_uri("http://18.220.122.33:5000")  # Set the tracking URI for MLflow
    mlflow.set_experiment("Cats and Dogs Classification")
    
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
