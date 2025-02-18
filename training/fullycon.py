import torch

FILTERS = 16
class CullyConnCoder (torch.nn.Module):
    def __init__(self, field_size):
        super(CullyConnCoder, self).__init__()
        self.size = int(field_size)
        # self.nekaj = int(self.size/2)

        self.conv1 = torch.nn.Conv2d(1, 8, 3, padding=1, )
        self.conv2 = torch.nn.Conv2d(8, FILTERS, 3, padding=1)
       
        self.linear = torch.nn.Sequential(
            torch.nn.Linear(FILTERS*FILTERS*FILTERS, 128),
            torch.nn.ReLU(inplace=True),

            torch.nn.Linear(128, 128),
            # torch.nn.Dropout(0.15),
            torch.nn.ReLU(inplace=True),

            # torch.nn.Linear(128, 128),
            # torch.nn.Dropout(0.3),
            # torch.nn.ReLU(inplace=True),

            # torch.nn.Linear(128, 128),
            # torch.nn.Dropout(0.15),
            # torch.nn.ReLU(inplace=True),

            torch.nn.Linear(128, self.size*self.size),
            torch.nn.LogSigmoid(),
        )

        # self.linear2 = torch.nn.Sequential(
        #     torch.nn.Linear(self.size*self.size, 64),
        #     torch.nn.ReLU(inplace=True),

        #     torch.nn.Linear(64, self.size*self.size),
        #     torch.nn.Sigmoid(),
        # )

        # self.end_conv = torch.nn.Sequential(
        #     torch.nn.Conv2d(1, 1, 3, padding=1, stride=1),
        #     torch.nn.ReLU(),
        #     torch.nn.Conv2d(1, 1, 3, padding=1, stride=1),
        #     torch.nn.ReLU(),
        # )



        # self.l1 = torch.nn.Linear(self.size * self.size, 50)
        # self.l2 = torch.nn.Linear(50, 50)
        # self.l3 = torch.nn.Linear(50, self.size*self.size)

    def forward(self, x:torch.Tensor):
        x = x.float()
        out = x
        out = self.conv1(out)
        out = torch.nn.functional.relu(out)

        out = self.conv2(out)
        out = torch.nn.functional.relu(out)
        # print("convolved", x.shape)
        
        out = out.view(-1, FILTERS*self.size*self.size)
        # print("input", x.shape)
        out = self.linear(out)
        out = out.view(-1, 1, self.size, self.size)

        # skip conn
        # out = torch.concat(out, x).clamp(0, 1)
        
        # out = out.view(-1, 1, self.size, self.size)
        # out = self.end_conv(out)

        return out
    