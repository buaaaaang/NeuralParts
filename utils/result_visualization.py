import torch
import trimesh
import os, sys
sys.path.insert(0, os.getcwd()) 
from model import Model, Model_overall
from dataloader.dataloader import build_dataloader
from loss.loss_function import loss_function
from metric.metric_function import metric_function
import utils.get_points_from_sphere as gs
from dataloader.dataset import build_dataset
import matplotlib.pyplot as plt
from simple_3dviz import Mesh
from simple_3dviz.scenes import Scene
from simple_3dviz.utils import save_frame

def visualize_result(model_path, index):
    device =  torch.device('cpu')
    model = Model(device)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.set_new_device(device)
    target, mesh_path = build_dataset('dfaust', ['train']).get(index) #6000
    print("result for", mesh_path)
    for i in range(len(target)):
        target[i] = target[i].to(device)
    num_points = 60 ** 2 - 60 * 2 + 2
    prediction = model.primitive_points(target, num_points)
    p_p = prediction
    B, n_points, n_primitives, D = p_p.shape


    face = (gs.fx_sample_face(B, num_points, n_points, d=3, randperm=False))
    for j in range(n_primitives):
        c = p_p[0, :, j, :].cpu().detach().numpy()
        r = trimesh.Trimesh(c, face)
        r.export(file_obj=("./result/prim_" + str(j) + ".obj"), file_type='obj')

    Listmesh = []
    for j in range(n_primitives):
        c = p_p[0, :, j, :].cpu().detach().numpy()
        #print("shape of c is : " + str(len(c)) + " * " + str(len(c[0])))
        Listmesh.append(trimesh.Trimesh(c, face))
    trimesh.util.concatenate(Listmesh).export(file_obj=("./result/overall.obj"), file_type='obj')
    render_mesh("./result/overall.obj", "./result/rendered_overall.png")
    render_mesh(mesh_path, "./result/rendered_gt.png")
    render_colored_mesh(n_primitives, "./result/rendered_overall_colored.png")
    print("done")

def get_scene():
    scene = Scene((1024, 1024))
    scene.camera_position = (0.55, 1.05, 1.65)
    scene.camera_target = (0, 0.35, 0)
    scene.light = (1, 1.5, 3)
    scene.up_vector = (0, 1, 0)

    return scene

def render_mesh(file_name, save_path):
    scene = get_scene()
    mesh = Mesh.from_file(file_name)
    scene.add(mesh)
    scene.render()
    save_frame(save_path, scene.frame)

def render_colored_mesh(n_primitives, save_path):
    scene = get_scene()
    color_list = [(0,0,1),(0,1,0),(1,0,0),(0.5,0.5,0),(0.5,0,0.5),(0,0.5,0.5),(0.5,0.5,0.5),(1,1,0),(1,0,1),(1,1,0)]
    for i in range(n_primitives):
        file_name = "./result/prim_" + str(i) + ".obj"
        mesh = Mesh.from_file(file_name, color=color_list[i])
        scene.add(mesh)
    scene.render()
    save_frame(save_path, scene.frame)

if __name__=='__main__':
    if (len(sys.argv) < 2):
        model_path = "./models/trained_model_5_prim.pth"
    else:
        model_path = sys.argv[1]
    visualize_result(model_path, 0) #5000 #7200 #6000
