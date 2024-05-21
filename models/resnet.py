import torch


class softmaxLegit2D(torch.nn.Module):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
    
    def forward(self, x):
        ex = torch.exp(x)
        return ex / (torch.sum(ex, dim=(2,3)).unsqueeze(-1).unsqueeze(-1) + 1e-15)
    
def rms_norm(tensor, norm_weights):
    return (tensor * torch.rsqrt(tensor.pow(2).mean(-1, keepdim=True) + 1e-05)) * norm_weights
    
    
class BasicBlock(torch.nn.Module):
    expansion = 1

    def __init__(self, inplanes, planes, stride=1):
        super(BasicBlock, self).__init__()
        
        self.conv1 = torch.nn.Conv2d(inplanes, planes, 3, 1, 1)
        self.bn1 = torch.nn.BatchNorm2d(planes)
        self.relu = torch.nn.ReLU(inplace=True)
        self.conv2 = torch.nn.Conv2d(planes, planes, 3, 1, 1)
        self.bn2 = torch.nn.BatchNorm2d(planes)
        if inplanes != planes:
            self.cconv = torch.nn.Conv2d(inplanes, planes, 3, 1, 1)
        self.stride = stride

    def forward(self, x):
        identity = x
        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)

        out = self.conv2(out)
        out = self.bn2(out)
        # print(out.shape, identity.repeat(1, out.shape[1]//identity.shape[1], 1, 1).shape)
        if out.shape != identity.shape:
            out += self.cconv(identity)
        else:
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
        # self.b3 = BasicBlock(16, 16)
        # self.b4 = BasicBlock(16, 16)
        # self.b5 = BasicBlock(16, 16)
        self.b6 = BasicBlock(16, 16)

        # self.b7 = BasicBlock(16, 1)
        self.b7 = torch.nn.Conv2d(16, 16, 3, 1, 1)
        self.outconv = torch.nn.Conv2d(16, 1, 3, 1, 1)


    
    def place(self, x, mask):
        # stich mask and input 
        batch_dim = x.shape[0]
        repeated_mask = mask.unsqueeze(0).repeat(batch_dim,1,1,1)
        x = torch.concat([repeated_mask, x], dim=1)
        x = x.float()

        # model
        out = self.b1(x)

        out = self.b2(out)
        # out = self.b3(out)
        # out = self.b4(out)
        # out = self.b5(out)
        out = self.b6(out)
        # print(x.repeat(1,b3.shape[1]//2, 1, 1))
        out = out + x.repeat(1,out.shape[1]//2, 1, 1)

        out = self.b7(out)
        out = self.outconv(out)

        return out
