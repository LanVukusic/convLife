import torch

class ConvolutionalAutoencoder (torch.nn.Module):
    def __init__(self, field_size):
        super(ConvolutionalAutoencoder, self).__init__()
        self.size = int(field_size)
        self.nekaj = int(self.size/2)

        self.encoder = torch.nn.Sequential(
            torch.nn.Conv2d(1,16, 3, stride=1, padding=1),
            torch.nn.ReLU(),
            #torch.nn.MaxPool2d(2, stride=1),
            torch.nn.Conv2d(16, 16, 3, stride=2, padding=1),
            torch.nn.ReLU(),
            #torch.nn.MaxPool2d(2, stride=1)
        )

        self.linear = torch.nn.Sequential(
            torch.nn.Linear(16*self.nekaj*self.nekaj, 100),
            torch.nn.ReLU(),
            torch.nn.Linear(100, 16*self.nekaj*self.nekaj),
            torch.nn.ReLU()
        )

        self.decoder = torch.nn.Sequential(
            torch.nn.ConvTranspose2d(16, 16, 3, stride=2, padding=1, output_padding=1),
            torch.nn.ReLU(),
            torch.nn.Conv2d(16, 8, 3, stride=1, padding=1),
            torch.nn.ReLU(),
            torch.nn.Conv2d(8, 1, 3, stride=1, padding=1),
            torch.nn.ReLU(),
            # torch.nn.ConvTranspose2d(8, 1, 3, stride=2, padding=1, output_padding=1),
            torch.nn.Softmax2d()
        )
    
    def forward(self, x):
        x = x.float()
        # print("input", x.shape)
        x = self.encoder(x)
        # print("encoded", x.shape) # 16, 32, 32
        x = x.view(-1, 16*self.nekaj*self.nekaj)
        # print("reshaped", x.shape)
        x = self.linear(x)
        # print("linear", x.shape)
        x = x.view(-1, 16, self.nekaj, self.nekaj)
        # print("unflattened", x.shape)
        x = self.decoder(x)

        return x
    