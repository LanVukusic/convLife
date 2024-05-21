from collections import deque, namedtuple
import random
import torch
from game_of_life import Game_of_life
from matplotlib import pyplot as plt

device = "cuda" if torch.cuda.is_available() else "cpu"


Transition = namedtuple('Transition',
                        ('state', 'action', 'next_state', 'reward'))


class ReplayMemory(object):

    def __init__(self, capacity):
        self.memory = deque([], maxlen=capacity)

    def push(self, state, action, next_state, reward):
        """Save a transition"""
        for b in range(state.shape[0]):
            self.memory.append(Transition(state[b].unsqueeze(0), action[b].unsqueeze(0), next_state[b].unsqueeze(0), reward[b]))

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)

# def get_choice2(batch:torch.Tensor):
#     out = (batch > 0.8).int()
#     return out
    
def get_choice(batch:torch.Tensor):
    shp = batch.shape[1:]
    size = batch.shape[-1]
    flt = batch.flatten(1,-1)
    a = torch.argmax(flt, dim=1).int()
    out = torch.zeros_like(flt)
    for o, a_i in zip(out, a):
        o[a_i] = 1
    out2 = out.unflatten(dim=1, sizes=shp).int()
    # print("get_choice_out",out2.shape,  out2[0])
    return out2

    # pixle_place_mask = (batch == torch.amax(batch, dim=(2,3)).unsqueeze(-1).unsqueeze(-1).repeat((1,1,size,size))).int()
    # print("ppm", pixle_place_mask[0][0])
    # if torch.sum(pixle_place_mask) != batch.shape[0]:
    #     raise Exception(f"JOJ NE! {torch.sum(pixle_place_mask)} ni {batch.shape[0]}")
    # return pixle_place_mask
    
def select_action(state:torch.Tensor, eps_threshold:float, policy_net:torch.nn.Module, mask:torch.Tensor) -> torch.Tensor:
    sample = random.random()
    # eps_threshold = EPS_END + (EPS_START - EPS_END) * \
    #     math.exp(-1. * steps_done / EPS_DECAY)
    if sample > eps_threshold:
        with torch.no_grad():
            # t.max(1) will return the largest column value of each row.
            # second column on max result is index of where max element was
            # found, so we pick action with the larger expected reward.
            # choices = torch.zeros_like(state)
            # for _ in max_moves:
            # print("select_action", state.shape, mask.shape)
            # print("neki")
            out = policy_net.place(state, mask)
            # plt.imshow(out[0][0].cpu().numpy())
            # plt.show()
            # print(out[0])
            return get_choice(out)
            # return get_choice(out)
                # state += choice

    else:
        # print("FAKE RANDOM")
        # return get_choice(policy_net.place(state, mask))
        # print("rnd")
        return get_choice(torch.rand(state.shape, dtype=torch.float)).to(device)
        # return torch.tensor([[env.action_space.sample()]], device=device, dtype=torch.long)

class GameEnv():
    def __init__(self, size, batch_size, mask) -> None:
        self.size = size
        self.batch_size = batch_size
        self.game = Game_of_life(self.size).to(device)
        self.state = self.reset()
        self.mask = mask.to(device)
        self.actions = []

    def reset(self):
        self.actions = []
        # with torch.no_grad():
            # game.cuda()
            # random binary noise of size size x size
            # prev_batch = torch.randint(0, 2, (self.batch_size, 1, self.size, self.size)).to(device)
            # prev_batch.cuda()
            # batch = self.game(prev_batch)
            # for i in range(random.randint(1,5)):
            #     batch, prev_batch = self.game(batch), batch
        # self.state = batch
        self.state = torch.zeros((self.batch_size, 1, self.size, self.size)).to(device)
        return self.state 

    def step(self, action):
        self.actions.append(action)
        # self.state = self.game((self.state + action) % 2)
        self.state = (self.state + action) % 2
        return self.state, self.reward()
    
    def reward(self):
        # mask_pixles_count = torch.sum(self.mask)
        inside = torch.sum(self.state * self.mask, (2,3))
        outside = torch.sum(self.state * ((self.mask + 1) % 2), (2,3))
        # out = torch.sum(torch.square(self.state - self.mask), (2,3))
        # print(out.shape)
        out = inside -  outside / 10
        # out = torch.nn.functional.sigmoid(out/20.0)*20.0
        return out
        # print(torch.argmax(torch.argmax(self.actions[-1], dim=-1), dim=-1).shape)
        # return torch.argmax(torch.argmax(self.actions[-1], dim=-1), dim=-1)