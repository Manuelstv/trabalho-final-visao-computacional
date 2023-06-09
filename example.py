import argparse
#from spherenet import OmniCustom
from spherenet import SphereConv2D, SphereMaxPool2D
import torch
from torch import nn
import torch.nn.functional as F
import numpy as np
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
from torchvision import transforms
import torchvision.datasets as datasets
from equi_conv import EquiConv2d, equi_conv2d
torch.cuda.empty_cache()


class SphereTat(nn.Module):
    def __init__(self):
        super(SphereTat, self).__init__()
        self.conv1 = EquiConv2d(3, 3*2, stride=1)
        self.pool1 = SphereMaxPool2D(stride=2)
        self.conv2 = EquiConv2d(3*2, 3*4, stride=1)
        self.pool2 = SphereMaxPool2D(stride=2)
        self.conv3 = EquiConv2d(3*4, 3*8, stride=1)
        self.pool3 = SphereMaxPool2D(stride=2)
        self.conv4 = EquiConv2d(3*8, 3*16, stride=1)
        self.pool4 = SphereMaxPool2D(stride=2)
        self.conv5 = EquiConv2d(3*16, 3*32, stride=1)
        self.pool5 = SphereMaxPool2D(stride=2)
        self.conv6 = EquiConv2d(3*32, 3*64, stride=1)
        self.pool6 = SphereMaxPool2D(stride=2)
        self.conv7 = EquiConv2d(3*64, 3*128, stride=1)
        self.pool7 = SphereMaxPool2D(stride=2)
        self.conv8 = EquiConv2d(3*128, 3*256, stride=1)
        self.pool8 = SphereMaxPool2D(stride=2)
        self.conv9 = EquiConv2d(3*256, 3*512, stride=1)
        self.pool9 = SphereMaxPool2D(stride=2)
        self.fully = nn.Sequential(nn.Linear(8064, 16128), nn.Dropout(0.5), nn.Linear(16128, 2))

    def forward(self, x):
        x = F.relu(self.pool1(self.conv1(x)))
        x = F.relu(self.pool2(self.conv2(x)))
        x = F.relu(self.pool3(self.conv3(x)))
        x = F.relu(self.pool4(self.conv4(x)))
        x = F.relu(self.pool5(self.conv5(x)))
        x = F.relu(self.pool6(self.conv6(x)))
        x = F.relu(self.pool7(self.conv7(x)))
        #x = F.relu(self.pool8(self.conv8(x)))
        #x = F.relu(self.pool9(self.conv9(x)))
        print(x.size())
        x = x.view(-1, 8064)  # flatten, [B, C, H, W) -> (B, C*H*W)
        x = self.fully(x)        
        return x 

class SphereNet(nn.Module):
    def __init__(self):
        super(SphereNet, self).__init__()
        self.conv1 = SphereConv2D(3, 3*2, stride=1)
        self.pool1 = SphereMaxPool2D(stride=2)
        self.conv2 = SphereConv2D(3*2, 3*4, stride=1)
        self.pool2 = SphereMaxPool2D(stride=2)
        self.conv3 = SphereConv2D(3*4, 3*8, stride=1)
        self.pool3 = SphereMaxPool2D(stride=2)
        self.conv4 = SphereConv2D(3*8, 3*16, stride=1)
        self.pool4 = SphereMaxPool2D(stride=2)
        self.conv5 = SphereConv2D(3*16, 3*32, stride=1)
        self.pool5 = SphereMaxPool2D(stride=2)
        self.conv6 = SphereConv2D(3*32, 3*64, stride=1)
        self.pool6 = SphereMaxPool2D(stride=2)
        self.conv7 = SphereConv2D(3*64, 3*128, stride=1)
        self.pool7 = SphereMaxPool2D(stride=2)
        self.conv8 = SphereConv2D(3*128, 3*256, stride=1)
        self.pool8 = SphereMaxPool2D(stride=2)
        self.conv9 = SphereConv2D(3*256, 3*512, stride=1)
        self.pool9 = SphereMaxPool2D(stride=2)
        self.fully = nn.Sequential(nn.Linear(3072, 6144), nn.Dropout(0.5), nn.Linear(6144, 2))

    def forward(self, x):
        x = F.relu(self.pool1(self.conv1(x)))
        x = F.relu(self.pool2(self.conv2(x)))
        x = F.relu(self.pool3(self.conv3(x)))
        x = F.relu(self.pool4(self.conv4(x)))
        x = F.relu(self.pool5(self.conv5(x)))
        x = F.relu(self.pool6(self.conv6(x)))
        x = F.relu(self.pool7(self.conv7(x)))
        x = F.relu(self.pool8(self.conv8(x)))
        x = F.relu(self.pool9(self.conv9(x)))
        #print(x.size())
        x = x.view(-1, 3072)  # flatten, [B, C, H, W) -> (B, C*H*W)
        x = self.fully(x)        
        return x 
         
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(3, 3*2, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(3*2, 3*4, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(3*4, 3*8, kernel_size=3, padding=1)
        self.conv4 = nn.Conv2d(3*8, 3*16, kernel_size=3, padding=1)
        self.conv5 = nn.Conv2d(3*16, 3*32, kernel_size=3, padding=1)
        self.conv6 = nn.Conv2d(3*32, 3*64, kernel_size=3, padding=1)
        self.conv7 = nn.Conv2d(3*64, 3*128, kernel_size=3, padding=1)
        self.conv8 = nn.Conv2d(3*128, 3*256, kernel_size=3, padding=1)
        self.conv9 = nn.Conv2d(3*256, 3*512, kernel_size=3, padding=1)
        #self.conv6 = nn.Conv2d(512, 512, kernel_size=3, padding=1)
        #self.fc = nn.Linear(8192, 4096)
        self.fully = nn.Sequential(nn.Linear(3072, 6144), nn.Dropout(0.5), nn.Linear(6144, 2))

    def forward(self, x):
        x = F.relu(F.max_pool2d(self.conv1(x), 2))
        x = F.relu(F.max_pool2d(self.conv2(x), 2))
        x = F.relu(F.max_pool2d(self.conv3(x), 2))
        x = F.relu(F.max_pool2d(self.conv4(x), 2))
        x = F.relu(F.max_pool2d(self.conv5(x), 2)) 
        x = F.relu(F.max_pool2d(self.conv6(x), 2))
        x = F.relu(F.max_pool2d(self.conv7(x), 2))
        #x = F.relu(F.max_pool2d(self.conv8(x), 2)) 
        #x = F.relu(F.max_pool2d(self.conv9(x), 2))
        
        #print(x.size())
        x = x.view(-1, 3072) 
        x = self.fully(x)
        #print(x.size())
        return x

def train(args, model, device, train_loader, optimizer, epoch):
    model.train()
    train_loss = 0
    
    for batch_idx, (data, target) in enumerate(train_loader):
        optimizer.zero_grad()
        #if data.dim() == 3:
        #    data = data.unsqueeze(1)  # (B, H, W) -> (B, C, H, W)
        
        y_pred = model(data.to(device))
        #print(data.#shape)
        #y_pred = y_pred.squeeze(1)
        #target = target.squeeze(1)
        #target = torch.argmax(target, 4)
        target = target.to(device)
        
        #print(y_pred.shape)
        #print(target.shape)
        class_loss = F.cross_entropy(y_pred, target) 
        
        class_loss.backward()
        
        optimizer.step()
        train_loss += class_loss.item()
     
    train_loss /= len(train_loader.dataset)
    
    print('\n Train Loss: ', train_loss)

    return train_loss


def test(args, model, device, test_loader):
    model.eval()
    test_loss = 0
    correct = 0

    with torch.no_grad():
        for data, target in test_loader:
            #data, target = data.to(device), target.long().to(device)
            #if data.dim() == 3:
            #    data = data.unsqueeze(1)  # (B, H, W) -> (B, C, H, W)
                        
            y_pred = model(data.to(device))
            #y_pred = y_pred.squeeze(1)
            target = target.to(device)
            
            class_loss = F.cross_entropy(y_pred, target)
            test_loss += class_loss.item()
            y_pred  = y_pred.max(1, keepdim=True)[1]

            for n in range(target.shape[0]):
                if(y_pred[n]==target[n]):
                    correct += 1

            #print(y_pred, target)

    test_loss /= len(test_loader.dataset)
    print('\n Test Loss: ', test_loss)
    print('\n Accuracy: ', correct/len(test_loader.dataset))
    
    return(test_loss)

def main():
    # Training settings
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--batch-size', type=int, default=8, metavar='N',
                        help='input batch size for training')
    parser.add_argument('--test-batch-size', type=int, default=8, metavar='N',
                        help='input batch size for testing')
    parser.add_argument('--epochs', type=int, default=300, metavar='N',
                        help='number of epochs to train')
    parser.add_argument('--optimizer', type=str, default='adam',
                        help='optimizer, options={"adam, sgd"}')
    parser.add_argument('--lr', type=float, default=1E-5, metavar='LR',
                        help='learning rate')
    parser.add_argument('--momentum', type=float, default=0.9, metavar='M',
                        help='SGD momentum')
    parser.add_argument('--no-cuda', action='store_true', default=False,
                        help='disables CUDA training')
    parser.add_argument('--seed', type=int, default=1, metavar='S',
                        help='random seed')
    parser.add_argument('--log-interval', type=int, default=1, metavar='N',
                        help='how many batches to wait before logging training status')
    parser.add_argument('--save-interval', type=int, default=1, metavar='N',
                        help='how many epochs to wait before saving model weights')
    args = parser.parse_args()
    use_cuda = not args.no_cuda and torch.cuda.is_available()

    torch.manual_seed(args.seed)

    device = torch.device('cuda' if use_cuda else 'cpu')

    kwargs = {'num_workers': 0, 'pin_memory': True} if use_cuda else {}

    np.random.seed(args.seed)

    transform = transforms.Compose([
        # you can add other transformations in this list
        transforms.ToTensor(),
        #transforms.Grayscale()
    ])

        
    train_dataset = datasets.ImageFolder(
    #root='/media/bycrop/byCrop_Dataset/SUN3601024x512/pano1024x512/train',
    root = '/media/bycrop/byCrop_Dataset/SUN3601024x512/pano1024x512/train',
    transform=transform
    )

    test_dataset = datasets.ImageFolder(
    root='/media/bycrop/byCrop_Dataset/SUN3601024x512/pano1024x512/val',
    transform=transform
    )

    # training data loaders
    train_loader = DataLoader(
    train_dataset, batch_size=8, shuffle=True,
    num_workers=0, pin_memory=True
    )

    test_loader = DataLoader(
    test_dataset, batch_size=8, shuffle=True,
    num_workers=0, pin_memory=True
    )

    # Train
    sphere_model = SphereTat().to(device)
    model = Net().to(device)
    
    if args.optimizer == 'adam':
        sphere_optimizer = torch.optim.Adam(sphere_model.parameters(), lr=args.lr)
        optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)
    elif args.optimizer == 'sgd':
        sphere_optimizer = torch.optim.SGD(sphere_model.parameters(), lr=args.lr, momentum=args.momentum)
        optimizer = torch.optim.SGD(model.parameters(), lr=args.lr, momentum=args.momentum)
    
    loss_train=[]
    loss_train_std=[]
    loss_test=[]
    loss_test_std=[]

    for epoch in range(1, args.epochs + 1):
        ## SphereCNN
        print('{} Sphere CNN {}'.format('='*10, '='*10))
        loss_train.append(train(args, sphere_model, device, train_loader, sphere_optimizer, epoch))
        loss_test.append(test(args, sphere_model, device, test_loader))

        # Conventional CNN
        print('{} Conventional CNN {}'.format('='*10, '='*10))
        loss_train_std.append(train(args, model, device, train_loader, optimizer, epoch))
        loss_test_std.append(test(args, model, device, test_loader))


    #informar o vetor de Ã©pocas no lugar no np.array(list.........
    epochs = np.array(list(range(0,2*len(loss_train),2)))


    plt.figure(figsize=(10, 5))

    plt.plot(epochs, loss_train, 'r', label='Training Loss') # plotting t, a separately 
    plt.plot(epochs, loss_test, 'b', label='Validation Loss') # plotting t, b separately 
    plt.plot(epochs, loss_train_std, 'g', label='Training Loss std') # plotting t, a separately 
    plt.plot(epochs, loss_test_std, 'y', label='Validation Loss std') # plotting t, b separately 
    plt.legend(loc='upper right')
    plt.grid(linestyle=':')
    plt.xlabel('Epochs',fontsize=18)
    plt.ylabel('Loss',fontsize=18)

    plt.show()



if __name__ == '__main__':
    main()
