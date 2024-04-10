import torch

FILTERS = 16
class CullyConnCoder (torch.nn.Module):
    def __init__(self, field_size):
        super(CullyConnCoder, self).__init__()
        self.size = int(field_size)
        # self.nekaj = int(self.size/2)

        self.conv1 = torch.nn.Conv2d(1, 1, 3, padding=1, bias=True)
        self.conv2 = torch.nn.Conv2d(1, 1, 3, padding=1, bias=True)
        # self.batch1 = torch.nn.BatchNorm2d(8)
        # self.conv2 = torch.nn.Conv2d(1, 1, 3, padding=1, bias=True)
        # self.batch2 = torch.nn.BatchNorm2d(1)
        # self.conv3 = torch.nn.Conv2d(8, 8, 3, padding=1,)
        # self.conv4 = torch.nn.Conv2d(8, 8, 3, padding=1,)
        # self.conv5= torch.nn.Conv2d(8, 1, 3, padding=1,)
        
    def forward(self, x:torch.Tensor):
        x = x.float()
        out = x
        out = self.conv1(out)
        out = torch.nn.functional.relu(out)
        out = self.conv2(out)
        out = torch.nn.functional.relu(out)
        # out = self.batch1(out)
        # out = torch.nn.functional.relu(out)
        # out = self.conv2(out)
        # out = self.batch2(out)
        # out = torch.nn.functional.relu(out)
        # out = self.conv1(out)
        # out = self.batch1(out)
        # out = torch.nn.functional.relu(out)
        # out = self.conv2(out)
        # out = self.batch2(out)
        # out = torch.nn.functional.relu(out)
        # out = out + out1
        # out = self.conv3(out)
        # out2 = torch.nn.functional.relu(out)
        # out = self.conv4(out2)
        # out = torch.nn.functional.relu(out)
        # out = out + out2
        # out = self.conv5(out)
        # out = torch.nn.functional.relu(out)
        
        # out = torch.nn.functional.relu(out)

        # out = self.conv2(out)
        # out = torch.nn.functional.relu(out)
        # # print("convolved", x.shape)
        
        # out = out.view(-1, FILTERS*self.size*self.size)
        # # print("input", x.shape)
        # out = self.linear(out)
        # out = out.view(-1, 1, self.size, self.size)

        # skip conn
        # out = torch.concat(out, x).clamp(0, 1)
        
        # out = out.view(-1, 1, self.size, self.size)
        # out = self.end_conv(out)

        return out
    