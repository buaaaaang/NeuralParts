from config import *
from os.path import join, exists
import numpy as np
from PIL import Image
from torchvision.transforms import Normalize
import torch
import matplotlib.pyplot as plt

class Data_base():
    def path_to_mesh_file(self):
        raise NotImplementedError()

    def path_to_image_file(self):
        raise NotImplementedError()

    def path_to_surface_samples(self):
        raise NotImplementedError()

    def path_to_volume_samples(self):
        raise NotImplementedError()

    def get_image(self):
        raw_image = torch.from_numpy(np.transpose(np.array(
            Image.open(self.path_to_image_file()).convert("RGB"))))
        F = Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]) 
        return F(raw_image.float() / 255.0).float()

    def get_surface_samples(self):
        n_sample = n_surface_samples
        pre_sampled = np.load(self.path_to_surface_samples(), mmap_mode="r")
        n_pre = pre_sampled.shape[0]
        rand = int(np.random.rand() * (n_pre - n_sample))
        sampled_surface = torch.from_numpy(np.array(
            pre_sampled[rand:rand+n_sample]).astype(np.float32))
        # plt.scatter(sampled_surface[:,0], sampled_surface[:,1], s=1)
        # plt.savefig("surface_sample_plot.png")
        # exit(0)
        return sampled_surface.float()

    def get_volume_samples(self):
        loaded_file = np.load(self.path_to_volume_samples(), allow_pickle=True)
        point = loaded_file["points"]
        occ = loaded_file["occupancies"]
        n_in, n_out = occ.sum(), len(occ) - occ.sum()
        p = (n_out * occ + n_in * (1-occ)) / (n_in * n_out * 2)
        weight = np.float32(1.0/len(point)) / p
        index = np.random.choice(len(point), n_volume_samples, p=p)
        # plt.scatter(point[:,0] * (1-occ), point[:,1] * (1-occ), s=1, color='red')
        # plt.scatter(point[:,0] * occ, point[:,1] * occ, s=1)
        # plt.savefig("volume_sample_plot.png")
        # exit(0)
        return torch.cat((torch.from_numpy(point[index]), torch.stack((
                torch.from_numpy(occ[index]), 
                torch.from_numpy(weight[index])), dim=1)), dim=-1).float()

class Data_dfaust(Data_base):
    def __init__(self, datainfo):
        self.data_dir = datainfo[0]
        self.data_num = datainfo[1]

    def path_to_mesh_file(self):
        return join(dfaust_dataset_directory, self.data_dir, 
                dfaust_mesh_folder, self.data_num + '.obj')

    def path_to_image_file(self):
        return join(dfaust_dataset_directory, self.data_dir, 
                dfaust_image_folder, self.data_num + '.png')

    def path_to_surface_samples(self):
        return join(dfaust_dataset_directory, self.data_dir, 
                dfaust_surface_samples_folder, self.data_num + '.npy')

    def path_to_volume_samples(self):
        return join(dfaust_dataset_directory, self.data_dir, 
                dfaust_volume_samples_folder, self.data_num + '.npz')


    
