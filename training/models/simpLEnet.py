import torch

from resnet import BasicBlock, softmaxLegit2D

class SimLEnet (torch.nn.Module):
    def __init__(self, field_size):
        super(SimLEnet, self).__init__()
        self.size = int(field_size)
        self.cel = self.size
        self.pol = int(self.size/2)
        self.cetrt = int(self.size/4)

        self.b1 = BasicBlock(2, 16)
        self.b2 = BasicBlock(16, 1)
        self.outconv = torch.nn.Conv2d(1, 1, 3, 1, 1)

    
    def place(self, x, mask):
        # stich mask and input 
        batch_dim = x.shape[0]
        repeated_mask = mask.unsqueeze(0).repeat(batch_dim,1,1,1)
        x = torch.concat([repeated_mask, x], dim=1)
        x = x.float()

        # model
        out = self.b1(x)
        out = self.b2(out)
        out = self.outconv(out)

        # out = self.b2(out)
        # out = self.b3(out)
        # out = self.b4(out)
        # out = self.b5(out)
        # out = self.b2(out)
        # print(x.repeat(1,b3.shape[1]//2, 1, 1))
        # out = out + x.repeat(1,out.shape[1]//2, 1, 1)

        # out = self.norm(out)


        return out
