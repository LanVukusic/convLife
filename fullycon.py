import torch

FILTERS = 16
class LifeBlock(torch.nn.Module):
    def __init__(self):
        super(LifeBlock, self).__init__()

        self.conv = torch.nn.Conv2d(1, 1, 3, padding=1, bias=False)
        self.conv1 = torch.nn.Conv2d(1, 1, 1, padding=0, bias=True)
        self.conv2 = torch.nn.Conv2d(1, 1, 1, padding=0, bias=True)
        self.conv3 = torch.nn.Conv2d(1, 1, 1, padding=0, bias=True)
        self.conv4 = torch.nn.Conv2d(1, 1, 1, padding=0, bias=True)
        self.conv5 = torch.nn.Conv2d(1, 1, 1, padding=0, bias=True)
        self.conv6 = torch.nn.Conv2d(1, 1, 1, padding=0, bias=True)

        self.conv_end1 = torch.nn.Conv2d(7, 7, 1, padding=0, bias=True)
        self.conv_end2 = torch.nn.Conv2d(7, 7, 1, padding=0, bias=True)
        self.conv_end3 = torch.nn.Conv2d(7, 1, 1, padding=0, bias=True)

        
    def forward(self, x: torch.Tensor):
        x = x.float()
        out = self.conv(x)
        out = torch.concat([x, self.conv1(out), self.conv2(out), self.conv3(out),
                               self.conv4(out), self.conv5(out), self.conv6(out)], dim=1)
        out = torch.nn.functional.relu(out)
        out = self.conv_end1(out)
        out = torch.nn.functional.relu(out)
        out = self.conv_end2(out)
        out = torch.nn.functional.relu(out)
        out = self.conv_end3(out)
        out = torch.nn.functional.relu(out)

        return out
    

class CullyConnCoder (torch.nn.Module):
    def __init__(self, field_size):
        super(CullyConnCoder, self).__init__()
        self.model = torch.nn.Sequential(
            LifeBlock(),
            LifeBlock()
        )
        
        
    def forward(self, x: torch.Tensor):
        return self.model(x)