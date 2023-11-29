import argparse
import torch
from torch.utils.data import DataLoader
import torchvision.datasets as datasets
from torchvision import transforms



def test(model_path, test_dataset, batch_size):
    # device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    device = torch.device('cpu')

    print(f'Loading Model at {model_path}')
    model = torch.load(model_path, map_location=torch.device('cpu'))
    model = model.to(device)
    first_layer = next(model.children())
    input_height = first_layer.kernel_size[0]
    input_width = first_layer.kernel_size[1]

    print(f'Input Size is: {input_height}x{input_width}')

    print(f'Loading Dataset at {test_dataset}')
    transform = transforms.Compose([
        transforms.RandomResizedCrop((input_height, input_width)),
        transforms.ToTensor()
    ])

    target_transform = transforms.Compose([
		lambda label: torch.nn.functional.one_hot(torch.tensor(label), num_classes = 3).float()
    ])
    
    dataset = datasets.ImageFolder(
        test_dataset,
        transform = transform,
        target_transform = target_transform
    )

    testloader = DataLoader(
        dataset,
        batch_size = batch_size,
    )

    print(f'Calculating Score')
    model.eval()  # Set the model to evaluation mode

    counter = 0
    total = 0

    with torch.no_grad():
        for images, labels in testloader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            accuracy = outputs.argmax(dim=1) == labels.argmax(dim=1)
            total += accuracy.int().sum()
            counter += len(images)

        score = total / counter * 100
        print(f'Score is: {score}')
        
        return score * 100

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dataset')
    parser.add_argument('-m', '--model')
    parser.add_argument('-b', '--batch_size', default = 32)
    args = parser.parse_args()
    test(args.model, args.dataset, args.batch_size)