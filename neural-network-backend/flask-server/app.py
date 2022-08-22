from flask import Flask, request, current_app
from werkzeug.utils import secure_filename
import os
import requests
import sys
import json
from PIL import Image

# adding Folder_2 to the system path
sys.path.insert(0, './modules')

from kissakoiratunnistus import ennustus 
from kissakoirauudelleenkoulutus import uudelleenkoulutus
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = './uploads'

def printf(message):
    return print(message, file=sys.stderr)

@app.route("/", methods=["POST", "GET"])
def save_file():

    if request.method == 'POST':

        try:


  #Tässä vastaanotetaan file
          f = request.files["file"]
          arvo =str(request.form.get('arvo'))
          printf(arvo)

         # print(f,file=sys.stderr)
  # laitetaan static kansioon
          path = os.path.join(app.config["UPLOAD_FOLDER"], f.filename)

  # Tässä tallennetaan tiedosto
          
          f.save(path)

  # Tässä palauttaa messagekoodin 200 ja json
         # send_file()
          tulos = ennustus()
          if arvo == "0":
              os.replace(path,f'./koulutus/kissa/{f.filename}')
          else:
              os.replace(path,f'./koulutus/koira/{f.filename}')


          printf(tulos)
          return tulos

          
          
        except Exception as error:
          print(error, file=sys.stderr)


@app.route("/retraini", methods=["POST", "GET"])
def retrain():

    if request.method == 'GET':
        koulutus = uudelleenkoulutus()
        printf(koulutus)
        return koulutus

@app.route("/palautus", methods=["POST", "GET"])
def palautus():

    if request.method == 'GET':

        osoite = './modules/kissakoirakoulutus2.pth'
        if os.path.isfile(osoite) ==  True:

            os.remove(osoite)
            vastaus = 'verkko palautettu alkuperäiseen'
        else:
            vastaus = 'verkko on jo palautettu!' 
        
        return vastaus




if __name__ == "__main__":
    app.run(debug=True)
