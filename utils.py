import numpy as np
import os

import torch
import torch.nn as nn
import torch.nn.functional as F
from PIL import Image
import torch.utils.data as data
import random


# Seed all possible
seed_ = 2026
random.seed(seed_)
np.random.seed(seed_)
torch.manual_seed(seed_)

# If using CUDA, you can set the seed for CUDA devices as well
if torch.cuda.is_available():
    torch.cuda.manual_seed(seed_)
    torch.cuda.manual_seed_all(seed_)
    
import torch.backends.cudnn as cudnn
cudnn.deterministic = True
cudnn.benchmark = False

class CatsAndDogsDataset(data.Dataset):
    def __init__(self, data_dir, target_size=(28, 28), color_mode='RGB', train=True):
        self.data_dir = data_dir
        self.target_size = target_size
        self.color_mode = color_mode
        self.classes = ['cats', 'dogs']
        self.train = train
        self.image_paths, self.labels = self.load_image_paths_and_labels()

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        image_path = self.image_paths[idx]
        image = Image.open(image_path)
        image = image.convert(self.color_mode)
        image = image.resize(self.target_size)
        image = np.array(image)
        image = (image / 255.0 - 0.5) / 0.5  # Normalize to range [-1, 1]
        image = torch.tensor(image, dtype=torch.float32)
        image = image.view(-1)

        label = torch.tensor(self.labels[idx], dtype=torch.long)

        return image, label

    def load_image_paths_and_labels(self):
        image_paths = []
        labels = []
        for class_idx, class_name in enumerate(self.classes):
            class_path = os.path.join(self.data_dir, 'train' if self.train else 'test', class_name)
            for filename in os.listdir(class_path):
                image_path = os.path.join(class_path, filename)
                image_paths.append(image_path)
                labels.append(class_idx)
        return image_paths, labels

class SimpleClassifier(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(SimpleClassifier, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = torch.relu(self.fc1(x))   # Feedforward step: Compute hidden layer activations
        x = self.fc2(x)              # Feedforward step: Compute output layer activations
        return F.log_softmax(x, dim=1)

# loss_history = [] # DO NOT DELETE

def train_model(model, input_size, train_loader, optimizer, criterion, epochs, loss_history):
    model.train()
    for epoch in range(epochs):
        running_loss = 0.0
        for inputs, labels in train_loader:
            inputs = inputs.view(-1, input_size)

            # Feedforward step: Compute the predicted output
            
            # Aprox 1 a 3 líneas (depende del acercamiento), la salida debe ser:
            # outputs = 
            # Pueden usar un acercamiento step-by-step (puntos extra)
            #     En esta deberían usar primero 
            hidden_layer_activations = torch.relu(torch.matmul(inputs, model.fc1.weight.T) + model.fc1.bias) # Usando torch.relu, torch.matmul
            output_layer_activations = torch.matmul(hidden_layer_activations, model.fc2.weight.T) + model.fc2.bias # Usando torch.matmul
            # O usar una forma más directa
            outputs = F.log_softmax(output_layer_activations, dim=1)

            # Compute the cost (loss)
            
            # Aprox 1 linea para calculo de la perdida
            loss = criterion(outputs, labels)
            
            # Backpropagation step: Compute gradients of the loss with respect to the model's parameters
            
            # Aprox 2 lineas para:
            # Limpiar gradientes previas usnado el optimizer
            # Computar las gradientes usando autograd
            optimizer.zero_grad()
            loss.backward()

            # Update the model's parameters using the computed gradients
            
            # Aprox 1 linea para:
            # Hacer un paso en la optimización, usar el optimizer
            optimizer.step()

            running_loss += loss.item()

        print(f"Epoch {epoch+1}/{epochs}, Loss: {running_loss/len(train_loader)}")
        loss_history.append(running_loss/len(train_loader))

    print("Training complete!")

def test_model(model, input_size, test_loader):
    """
    Evaluate the performance of a trained neural network model on the test data.
    
    Arguments:
    model: The trained neural network model to be evaluated.
    test_loader: The DataLoader containing the test data and labels.
    """
    
    model.eval()  # Set the model in evaluation mode

    correct = 0
    total = 0

    with torch.no_grad():
        for inputs, labels in test_loader:
            inputs = inputs.view(-1, input_size)
            labels = labels.view(-1)  # Reshape the labels to be compatible with NLLLoss()

            # Forward pass
            outputs = model(inputs)

            # Get predictions
            _, predicted = torch.max(outputs.data, 1)

            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    accuracy = 100 * correct / total
    print(f"Test Accuracy: {accuracy:.2f}%")
    return accuracy
