import torch
from model import Model, Model_overall
from dataloader.dataloader import build_dataloader
from loss.loss_function import loss_function
from metric.metric_function import metric_function
import os, sys

def main(model_path):
    device =  torch.device('cuda:0' if torch.cuda.is_available() else 'cpu' )
    model = Model(device)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.set_new_device(device)
    test_dataloader = build_dataloader('dfaust',['test'])
    loss_fn = loss_function
    metric_fn = metric_function
    sum_loss = [0.,0.,0.,0.,0.]
    sum_metric = [0.,0.]
    print("-----------------test-----------------\n")
    
    for b, target in zip(list(range(len(test_dataloader))), test_dataloader):
        for i in range(len(target)):
            target[i] = target[i].to(device)
        prediction = model(target)
        loss = loss_fn(prediction, target, sum_loss)
        loss.backward()
        metric_fn(prediction, target, sum_metric)
        sys.stdout.write("batch: %d, losses: %.5f, %.5f, %.5f, %.5f, %.5f, iou: %.5f, chamferL1: %.5f \r" % (b+1, sum_loss[0]/(b+1), sum_loss[1]/(b+1), sum_loss[2]/(b+1), sum_loss[3]/(b+1), sum_loss[4]/(b+1), sum_metric[0]/(b+1), sum_metric[1]/(b+1)))
    print("\n")
    print("--------------------------------------")


if __name__=='__main__':
    if (len(sys.argv) < 2):
        model_path = "./models/trained_model_5_prim.pth"
    else:
        model_path = sys.argv[1]
    main(model_path)