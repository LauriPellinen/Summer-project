import torch
from torch import nn, optim
import torch.nn.functional as F
from torchvision import datasets, transforms, models
import sys
from collections import OrderedDict

#Ladataan testi.pth tiedoston state_dict, map_locationilla määritellään tämän olevan cpu, sillä gpu tukea kontissa ei vielä ole.

import os
x = "./modules/testi1.pth"
y = "./modules/kissakoirakoulutus2.pth"
if os.path.exists(y) == True:
    x = y
state_dict = torch.load(x, map_location=torch.device('cpu'))
# Malli modelssilta, käytetään densenet121
model = models.densenet121(pretrained=True)

# Freezaa parametrit, ettei backproppia
for param in model.parameters():
    param.requires_grad = False
    #classifierin kerrokset, ReLU ja outputtiin LogSoftMax
model.classifier = nn.Sequential(nn.Linear(1024, 512),
                                 nn.ReLU(),
                                 nn.Dropout(0.2),
                                 nn.Linear(512, 256),
                                 nn.ReLU(),
                                 nn.Dropout(0.1),
                                 nn.Linear(256, 2),
                                 nn.LogSoftmax(dim=1))
# loss funktio
criterion = nn.NLLLoss() 

#optimizer mallilla, käytetään Adamia
optimizer = optim.Adam(model.classifier.parameters(), lr=0.003)

model.load_state_dict(state_dict)

