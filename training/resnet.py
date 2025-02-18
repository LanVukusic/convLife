import torch

class softmaxLegit2D(torch.nn.Module):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
    
    def forward(self, x):
        ex = torch.exp(x)
        return ex / (torch.sum(ex, dim=(2,3)).unsqueeze(-1).unsqueeze(-1))
    
    
class BasicBlock(torch.nn.Module):
    expansion = 1

    def __init__(self, inplanes, planes, stride=1):
        super(BasicBlock, self).__init__()
        
        self.conv1 = torch.nn.Conv2d(inplanes, planes, 3, 1, 1)
        self.bn1 = torch.nn.BatchNorm2d(planes)
        self.relu = torch.nn.ReLU(inplace=True)
        self.conv2 = torch.nn.Conv2d(planes, planes, 3, 1, 1)
        self.bn2 = torch.nn.BatchNorm2d(planes)
        self.stride = stride

    def forward(self, x):
        out = self.conv1(x)
        identity = out
        out = self.bn1(out)
        out = self.relu(out)

        out = self.conv2(out)
        out = self.bn2(out)

        out += identity
        out = self.relu(out)

        return out


class KaoResnet (torch.nn.Module):
    def __init__(self, field_size):
        super(KaoResnet, self).__init__()
        self.size = int(field_size)
        self.cel = self.size
        self.pol = int(self.size/2)
        self.cetrt = int(self.size/4)

        self.b1 = BasicBlock(2, 16)
        self.b2 = BasicBlock(16, 16)
        self.b3 = BasicBlock(16, 16)

        self.b4 = BasicBlock(16, 1)
        self.soft = softmaxLegit2D()

    
    def place(self, x, mask):
        # stich mask and input 
        batch_dim = x.shape[0]
        repeated_mask = mask.unsqueeze(0).repeat(batch_dim,1,1,1)
        x = torch.concat([repeated_mask, x], dim=1)
        x = x.float()

        # model
        b1 = self.b1(x)

        b2 = self.b2(b1)
        b3 = self.b3(b2)
        b3 = b3 + b1

        b4 = self.b4(b3)

        return self.soft(b4)
