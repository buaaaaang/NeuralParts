import torch

def loss_coverage(prediction, target, sum_loss):
    # target : occupancy pairs

    t_pts = target[2][:,:,:3] # batch * N * 3
    t_labels = target[2][:,:,3] # batch * N
    t_w = target[2][:,:,4] # batch * N
    
    g_m = prediction[1] # batch * N * M

    M = g_m.shape(2)
    t_labels_ext = torch.unsqueeze(dim=2).expand(-1, -1, M)
    
    Max = torch.abs(torch.max(g_m))
    t_labels_ext = (-2) * Max * t_labels_ext + g_m

    k = 10
    # for each primitive, we need to choose k points
    # whose value of g^m is the smallest.

    val, ind = torch.topk(t_labels_ext, k, dim=1, largest=False)
    # val : batch * k * M, ind : batch * k * M
    z = torch.zeros(val.shape)

    loss = (torch.sum(torch.maximum(val + (2*Max), z), dim = (1, 2)) * t_w).mean()
    sum_loss[4] += loss.item()
    return loss

    


