from IPython import display
import matplotlib.pyplot as plt
import numpy as np

def plot_state(state, actions, rewards, mask, first_model_preds):
  batch_size = state.shape[0]
  display.clear_output(wait=True)
  plotstate = state
  plotstate = plotstate.detach().cpu().squeeze(1).numpy()
  actions = actions.detach().cpu().squeeze(1).numpy()
  actions = (actions / np.max(actions))
  
  fig = plt.figure(figsize=(16,6))
  gs = fig.add_gridspec(3, state.shape[0],)

  # images for mask, actions, states
  for i in range(batch_size):
    image = np.zeros((3, state.shape[2], state.shape[3]))
    image[0, :, :] = plotstate[i]
    image[1, :, :] = actions[i]
    if mask != None:
      image[2, :, :] = mask[0].cpu().numpy()
    ax = fig.add_subplot(gs[0, i])
    ax.imshow(np.moveaxis(image, 0, -1))
    ax.set_xticks([])
    ax.set_yticks([])

  # loss graph
  ax = fig.add_subplot(gs[1, :])
  ax.axhline(y=0, c="black", alpha=0.2)
  r = np.array(rewards)
  r = r.T
  
  cmp = plt.get_cmap("viridis")
  xs = np.arange(len(rewards))
  for i in range(batch_size):
    ax.plot(xs, r[i], alpha=0.4, c=cmp(i*15))
  
  # model outputs
  for i in range(batch_size):
    ax = fig.add_subplot(gs[2, i])
    ax.imshow(first_model_preds[i][0])
    ax.set_xticks([])
    ax.set_yticks([])
  
  # model outputs
  # for i in range(batch_size):
  #   ax = fig.add_subplot(gs[3, i])
  #   ax.imshow(second_model_preds[i][0])
  #   ax.set_xticks([])
  #   ax.set_yticks([])
  
  plt.ioff()
  display.display(plt.gcf())
  plt.close(fig)