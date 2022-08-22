from kissakoiralataaja import *
import torch
from PIL import Image
import torchvision.transforms as transforms
import os
# tehdään funktio, jolla ennustetaan vastaanotettu kuva.

def ennustus():
    model.eval()

# Tällä loitsulla valitaan kansiossa oleva kuva, nimestä tai kuvamuodosta riippumatta, laitetaan se muuttujaan x
    for x in os.listdir("./uploads"):
        if x.endswith(".jpg") or x.endswith(".jpg") or x.endswith(".png") or x.endswith(".jpeg"):
        # Prints only text file present in My Folder
            picture = x
# Valitaan kuva PIL kirjaston kuvamuuttujaan
    image = Image.open('./uploads/'+ picture)

# Define a transform to convert the image to tensor
    transform = transforms.Compose([transforms.Resize(255), transforms.CenterCrop(224), transforms.ToTensor()])

# Muokataan kuva pytorchin tensoriksi
    tensorx = transform(image)

    tensorx = torch.unsqueeze(tensorx,0)

# Lasketaan todennäköisyydet kuvasta

    with torch.no_grad():
        output = model.forward(tensorx)

    ps = torch.exp(output)
    top_p, top_class = ps.topk(1, dim=1)
# # Jos ennustus on 0, laitetaan xy muuttujaksi kissa, jos taas 1, koira
    if top_class == 0:
        xy="kissa"
    elif top_class == 1:
        xy="koira"
    # palautetaan xy, joka voidaan sitten myöhemmin laittaa esim webbisivulle    
    return xy
