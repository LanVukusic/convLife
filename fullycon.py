import torch

FILTERS = 16
class CullyConnCoder (torch.nn.Module):
    def __init__(self, field_size):
        super(CullyConnCoder, self).__init__()
        self.size = int(field_size)
        # self.nekaj = int(self.size/2)

        self.conv1 = torch.nn.Conv2d(1, 9, 3, padding=1, bias=True)
        self.conv2 = torch.nn.Conv2d(9, 1, 3, padding=1, bias=True)
        # self.conv3 = torch.nn.Conv2d(9, 9, 3, padding=1, bias=True)
        # self.conv4 = torch.nn.Conv2d(9, 1, 3, padding=1, bias=True)

        
    def forward(self, x:torch.Tensor):
        x = x.float()
        out = x
        out = self.conv1(out)
        out = torch.nn.functional.relu(out)
        out = self.conv2(out)
        out = torch.nn.functional.relu(out)
        out = self.conv1(out)
        out = torch.nn.functional.relu(out)
        out = self.conv2(out)
        out = torch.nn.functional.relu(out)
        # out = self.conv3(out)
        # out = torch.nn.functional.relu(out)
        # out = self.conv4(out)
        # out = torch.nn.functional.relu(out)

        return out
    