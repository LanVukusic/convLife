import torch

class softmaxLegit2D(torch.nn.Module):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
    
    def forward(self, x):
        ex = torch.exp(x)
        return ex / torch.sum(ex, dim=(2,3)).unsqueeze(-1).unsqueeze(-1) 


class PointPainerModel (torch.nn.Module):
    def __init__(self, field_size):
        super(PointPainerModel, self).__init__()
        # bljak
        self.size = int(field_size)
        self.cel = self.size
        self.pol = int(self.size/2)
        self.cetrt = int(self.size/4)

        self.encoder1 = torch.nn.Sequential(
            torch.nn.Conv2d(2, 16, 3, stride=1, padding=1),
            torch.nn.ReLU(),
            #torch.nn.MaxPool2d(2, stride=1),
            torch.nn.Conv2d(16, 16, 3, stride=1, padding=1),
            torch.nn.ReLU(),
        )

        self.encoder2 = torch.nn.Sequential(
            torch.nn.Conv2d(16, 16, 3, stride=1, padding=1),
            torch.nn.ReLU(),
            #torch.nn.MaxPool2d(2, stride=1)
        )

        self.linear = torch.nn.Sequential(
            torch.nn.Linear(16*self.cel*self.cel, 100),
            torch.nn.ReLU(),
            torch.nn.Linear(100, 16*self.cel*self.cel),
            torch.nn.ReLU()
        )

        # placing policy π
        self.decoder1 = torch.nn.Sequential(
            torch.nn.Conv2d(16, 16, 3, stride=1, padding=1),
            torch.nn.ReLU(),
        )
        self.decoder2 = torch.nn.Sequential(
            # torch.nn.Conv2d(16, 8, 3, stride=1, padding=1),
            # torch.nn.ReLU(),
            torch.nn.Conv2d(16, 1, 3, stride=1, padding=1),
            softmaxLegit2D()
        )

        # placing prediction
        # self.placing = torch.nn.Sequential(
        #     torch.nn.Conv2d(16, 32, 3, stride=2, padding=1),
        #     torch.nn.ReLU(),
        #     torch.nn.Conv2d(32, 64, 3, stride=2, padding=1),
        #     torch.nn.ReLU(),
        #     torch.nn.Flatten(),
        #     torch.nn.Linear(64*self.cetrt*self.cetrt, 256),
        #     torch.nn.ReLU(),
        #     torch.nn.Linear(256, 128),
        #     torch.nn.ReLU(),
        #     torch.nn.Linear(128, 32),
        #     torch.nn.ReLU(),
        #     torch.nn.Linear(32, 2),
        #     torch.nn.Softmax()
        # )
    
    def place(self, x, mask):
        batch_dim = x.shape[0]
        repeated_mask = mask.unsqueeze(0).repeat(batch_dim,1,1,1)
        x = torch.concat([repeated_mask, x], dim=1)
        # print("x", x.shape)

        x = x.float()
        # print("input", x.shape)
        x_skip_1 = self.encoder1(x)
        x = self.encoder2(x_skip_1)
        # print("encoded", x.shape) # 16, 32, 32
        x = x.view(-1, 16*self.cel*self.cel)
        # print("reshaped", x.shape)
        x = self.linear(x)
        # print("linear", x.shape)
        x = x.view(-1, 16, self.cel, self.cel)
        # print("unflattened", x.shape)
        # print("prej", x.shape)
        x = self.decoder1(x)
        x = x + x_skip_1
        x = self.decoder2(x)
        

        # print("pol", x.shape)
        
        return x

    # def skip(self, x, mask):
    # batch_dim = x.shape[0]
    # repeated_mask = mask.unsqueeze(0).repeat(batch_dim,1,1,1)
    # x = torch.concat([repeated_mask, x], dim=1)

    #     x = x.float()
    #     # print("input", x.shape)
    #     x = self.encoder(x)
    #     # print("reshaped", x.shape)
    #     x = self.placing(x)
    #     return x