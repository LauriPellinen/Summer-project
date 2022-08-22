from kissakoiralataaja import *
import torch
from PIL import Image
import torchvision.transforms as transforms
import time

def uudelleenkoulutus():
    #select picture folder
    #picture_folders = 'loaded_picture'
    picture_folders = './koulutus/'

    #start training at least with 32 pictures
    if len(datasets.ImageFolder(picture_folders)) >= 32:
        model.train(mode=True)

        #Make pictures to tensor and make then same size.
        train_transforms = transforms.Compose([transforms.RandomRotation(30),
                                               transforms.RandomResizedCrop(224),
                                               transforms.RandomHorizontalFlip(),
                                               transforms.ToTensor(),
                                               transforms.Normalize([0.485, 0.456, 0.406],
                                                                    [0.229, 0.224, 0.225])])

        #Here you select folder and in folder there is folders with pictures. These subfolders does labeling for cats and dogs.
        train_data = datasets.ImageFolder(picture_folders, transform=train_transforms)

        #Here you select batch size and you can shuffle dataset
        trainloader = torch.utils.data.DataLoader(train_data, batch_size=32, shuffle=True)

    #Here we select old test pictures to test accuracy
        picture_folders2 = './vanhatkuvat/Cat_Dog_data'
        test_transforms = transforms.Compose([transforms.Resize(255),
                                              transforms.CenterCrop(224),
                                              transforms.ToTensor(),
                                              transforms.Normalize([0.485, 0.456, 0.406],
                                                                   [0.229, 0.224, 0.225])])
        test_data = datasets.ImageFolder(picture_folders2 + '/test', transform=test_transforms)
        testloader = torch.utils.data.DataLoader(test_data, batch_size=32)
        startti = time.time()
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model.to(device);
        epochs = 1
        steps = 0
        running_loss = 0
        print_every = 1
        for epoch in range(epochs):
            for inputs, labels in trainloader:
                steps += 1
                # Move input and label tensors to the default device
                inputs, labels = inputs.to(device), labels.to(device)
               # labels=labels-1
                logps = model.forward(inputs)
                loss = criterion(logps, labels)

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                running_loss += loss.item()

                if steps % print_every == 0:
                    test_loss = 0
                    accuracy = 0
                    model.eval()
                    with torch.no_grad():
                        for inputs, labels in testloader:
                            inputs, labels = inputs.to(device), labels.to(device)
                            logps = model.forward(inputs)
                            # If labels are are giving error run labels-1 because NN thinks cats are 1 and dogs are 2.
                            #labels=labels-1
                            batch_loss = criterion(logps, labels)

                            test_loss += batch_loss.item()

                            # Calculate accuracy
                            ps = torch.exp(logps)
                            top_p, top_class = ps.topk(1, dim=1)
                            equals = top_class == labels.view(*top_class.shape)
                            accuracy += torch.mean(equals.type(torch.FloatTensor)).item()

                    print(f"Epoch {epoch+1}/{epochs}.. "
                          f"Train loss: {running_loss/print_every:.3f}.. "
                          f"Test loss: {test_loss/len(testloader):.3f}.. "
                          f"Test accuracy: {accuracy/len(testloader):.3f}")
                    running_loss = 0
                    model.train()

        torch.save(model.state_dict(), './modules/kissakoirakoulutus2.pth')
        palautus = f"Test accuracy: {accuracy/len(testloader):.3f} and time: "
        aika = str(time.time() - startti) 
        dir = './koulutus/kissa/'
        dir2 = './koulutus/koira/'
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))
        for f in os.listdir(dir2):
            os.remove(os.path.join(dir2, f))
       # print(f"Test accuracy: {accuracy/len(testloader):.3f} and time :")
        return palautus+aika
    else:
        return "ei tarpeeksi kuvia"
    

