import torch
import matplotlib.pyplot as plt

class Game_of_life (torch.nn.Module):
    def __init__(self, size):
        super(Game_of_life, self).__init__()
        self.size = size
    
        self.conv = torch.nn.Conv2d(1, 1, 3, stride=1, padding=1, bias=False)
        self.conv.weight = torch.nn.Parameter(torch.tensor([[[[1, 1, 1], [1, 0, 1], [1, 1, 1]]]], requires_grad=False).float())
        self.lookup = torch.nn.Parameter(torch.tensor([0,0,0,1,0,0,0,0,0, 0,0,1,1,0,0,0,0,0], requires_grad=False).int(), requires_grad=False)

    def forward(self, x):
        neigh = self.conv(x.float()).int()
        out = self.lookup[neigh + x.int()*9]
        
        return out.view(-1, 1, self.size, self.size)
    

if __name__ == "__main__":
    size = 10
    model = Game_of_life(size)
    x = torch.zeros(1, 1, size, size).int()

    # plt.imshow(x[0].numpy().reshape(size, size,1), cmap='gray')
    # plt.show()

    x[0,0,4,4] = 1
    x[0,0,5,4] = 1
    x[0,0,6,4] = 1
    print(x.shape)
    out = model(x)
    print(out.shape)
    out = model(out)
    print(out)
    out = model(out)
    print(out)