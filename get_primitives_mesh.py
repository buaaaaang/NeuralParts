import torch
import trimesh
from model import Model, Model_overall
from dataloader.dataloader import build_dataloader
from loss.loss_function import loss_function
from metric.metric_function import metric_function
import utils.get_points_from_sphere as gs
from dataloader.dataset import build_dataset
import os, sys

def get_primitives_mesh():
    device =  torch.device('cpu')
    model = Model(device)
    model.load_state_dict(torch.load("model.pth", map_location=device))
    model.set_new_device(device)
    target = build_dataset('dfaust', ['train']).get(1)
    for i in range(len(target)):
        target[i] = target[i].to(device)
    prediction = model(target)
    p_p = prediction[0]
    B, n_points, n_primitives, D = p_p.shape
    assert (D == 3)
    face = (gs.fx_sample_face(B, n_points, n_primitives, d=3, randperm=False))
    print("face shape is : " + str(len(face)) + " * " + str(len(face[0])))
    print("face is : " + str(face))
    print("number of primitives : " + str(n_primitives))
    for j in range(n_primitives):
        c = p_p[0, :, j, :].cpu().detach().numpy()
        print("shape of c is : " + str(len(c)) + " * " + str(len(c[0])))
        r = trimesh.Trimesh(c, face)
        r.export(file_obj=("./mesh_00" + str(j) + ".obj"), file_type='obj')

get_primitives_mesh()

#class GPM(torch.nn.Module):
#    def __init__(self):
#        get_primitives_mesh()



    