import torch
from dataloader.dataloader import build_dataloader
from model import Model
from loss.loss_function import loss_function
from metric.metric_function import metric_function
import os
from config import *

def main():
    device =  torch.device('cuda:0' if torch.cuda.is_available() else 'cpu' )
    model = Model(device).to(device)
    train_dataloader = build_dataloader('dfaust',['train'])
    val_dataloader = build_dataloader('dfaust',['val'])
    loss_fn = loss_function
    metric_fn = metric_function
    optimizer = torch.optim.Adam(model.parameters(),lr=learning_rate)

    for epoch in range(n_epoch):
        aggregate = 0
        loss = torch.FloatTensor(0)
        sum_loss = [0.,0.,0.,0.,0.]
        sum_metric = [0.,0.]
        for b, target in zip(list(range(n_step_per_epoch)), train_dataloader.infinite_iterator()):
            aggregate += 1
            for i in range(len(target)):
                target[i] = target[i].to(device)
            prediction = model(target)
            loss = loss + loss_fn(prediction, target, sum_loss)
            metric_fn(prediction, target, sum_metric)
            sys.stdout.write("epoch %d, batch: %d, losses: %.5f, %.5f, %.5f, %.5f, %.5f, iou: %.5f, chamferL1: %.5f \r" % (epoch, b, sum_loss[0]/b, sum_loss[1]/b, sum_loss[2]/b, sum_loss[3]/b, sum_loss[4]/b, sum_metric[0]/b, sum_metric[1]/b))
            if (aggregate == n_aggregate):
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                aggregate = 0
                loss = torch.FloatTensor(0)
        print("epoch %d, batch: %d, losses: %.5f, %.5f, %.5f, %.5f, %.5f, iou: %.5f, chamferL1: %.5f \r" % (epoch, b, sum_loss[0]/b, sum_loss[1]/b, sum_loss[2]/b, sum_loss[3]/b, sum_loss[4]/b, sum_metric[0]/b, sum_metric[1]/b))
        if epoch != 0 and epoch % 10 == 0:
            printf("--------------validation--------------")
            sum_loss = [0.,0.,0.,0.,0.]
            sum_metric = [0.,0.]
            with torch.no_grad():
                for b, target in zip(list(range(len(val_dataloader))), val_dataloader):
                    for i in range(len(sample)):
                        target[i] = target[i].to(device)
                    prediction = model(target)
                    loss_fn(prediction, target, sum_loss)
                    metric_fn(prediction, target, sum_loss)
                    sys.stdout.write("epoch %d, batch: %d, losses: %.5f, %.5f, %.5f, %.5f, %.5f, iou: %.5f, chamferL1: %.5f \r" % (epoch, b, sum_loss[0]/b, sum_loss[1]/b, sum_loss[2]/b, sum_loss[3]/b, sum_loss[4]/b, sum_metric[0]/b, sum_metric[1]/b))
            print("epoch %d, batch: %d, losses: %.5f, %.5f, %.5f, %.5f, %.5f, iou: %.5f, chamferL1: %.5f \r" % (epoch, b, sum_loss[0]/b, sum_loss[1]/b, sum_loss[2]/b, sum_loss[3]/b, sum_loss[4]/b, sum_metric[0]/b, sum_metric[1]/b))
            printf("--------------------------------------")


if __name__=='__main__':
    main()