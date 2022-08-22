from flask import Flask, Blueprint, render_template, flash, redirect, request, session, abort, url_for, current_app
import sys
from werkzeug.utils import secure_filename
import os
import requests
import json
import base64

app = Flask(__name__)
app.config['SECRET_KEY'] = 'laurintekemäwebbisivu'
app.config["UPLOAD_FOLDER"] = './static/uploads'


# when saving the file



# Kotiosoitteen alussa testi, millä otetaan yhteys toisen koneen kotiosoitteeseen ja tulostetaan vastaus
# Homesivun alussa kirjautumisfunktio, eli tarkistetaan onko sessio logged in, jos ei -->
# palautetaan login funktiom joka siis /loginin alla, jos on, palautetaan home.html template käyttäen render_template kirjastoa
@app.route('/',methods=['GET', 'POST'])
def home():
    #r = requests.get('http://10.50.91.23:5000/')
    #print(r.text, 'teksti',file=sys.stderr)
    

    if not session.get('logged_in'):

        return login()
    else:
        return render_template("home.html")
    

# Login muuttujassa tarkastetaan, onko formeista username, sekä salasana tulevat tiedot täsmäävät.
# Alussa myös kysytään, jos method on GET, palautetaan login.html, jos POST, tehdään yllä mainittu tarkastus
# Jos salasanat ovat oikein, vaihdetaan session logged_iniksi
# lopuksi palautetaan kotifunktio.
@app.route('/login', methods=['GET', 'POST']) 
def login():
    if request.method == "GET":
        return render_template('login.html')
    elif request.method == "POST":
        if request.form.get('password') == 'projekti345' and request.form.get('username') == 'kesa123':

            session['logged_in'] = True
        else:
            flash('wrong password or username!')
        return home()
    else:
        return "Opetteleppa ajaa hommia"
# Logout funktiossa yksinkertaisesti kun logout osoitteeeseen ohjataan, vaihtaa se session logged_in tilaksi false ja
# palauttaa kotifunktion
@app.route("/logout",methods=['GET', 'POST'])
def logout():
    
    session['logged_in'] = False
    return home()
# Tässä osoitteessa käsitellään post request, jonka kautta kuva ladataan palvelimelle. Kuva tulee html formin kautta
# Tähän osoitteeseen, jossa se tallennetaan muuttujaan, joka tallentaa sen kansioon
# Määritellään kansio, sekä mikä on tämänhetkinen sijainti. Lopuksi palataan kotiosoitteeseen.
# Tätä tarkoitus muokata niin, että kuva lähetetään toiselle koneelle, jossa sen avulla ennustetaan.
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    url = 'http://10.50.91.23:5000/'
    if request.method == 'POST':
        # Jos ei ole mitään queryssa, valittaa että ei oo kuvvaa, en oo jaksanu vielä tehä sellasta kohtaa, että
        # ei voi painaa nappia ollenkaan
        if not request.files.get('file', None):
            error = "No file selected"
            flash(error)
        else:
            # otetaan formilta tullut file
            f= request.files['file']
            arvo= request.form.get('arvo')
            
            
            #path = os.path.join(app.config["UPLOAD_FOLDER"], f.filename)
            #f.save(path)
            image_string = str(base64.b64encode(f.read()).decode())
            image = "data:image/png;base64," + image_string
            
            # tämä taikatemppu auttaa kuvan displayaamisessa, sekä siinä ettei se mee rikki. Eli palauttaa kuvan jotenkin alkuun
            f.seek(0)
            # Määritetään filen nimi, stream= imagen data mimetype= esimerkiksi kuvan tyyppi (jpg png etc.)
            files = {"file": (f.filename, f.stream, f.mimetype)}

            #UPLOADS_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static/',f.filename)
            path = os.path.join(app.config["UPLOAD_FOLDER"], f.filename)
            # Lähetetään requests kirjaston postilla

            
            
            r = requests.post(url=url,files=files,  data={'arvo': arvo})
            response = r.text 

            print(response, file=sys.stderr)

            


            return render_template("result.html", image=image, result=response)
            #f.save(path)
            
            
            
            #return home()


@app.route("/retrain",methods=['GET', 'POST'])
def retrain():
    if request.method == 'GET':

        rr = requests.get('http://10.50.91.23:5000/retraini')
        print(rr.text, file=sys.stderr)
        flash(rr.text, category='info')
    return home()


@app.route("/palautus",methods=['GET', 'POST'])
def palautus():
    if request.method == 'GET':

        rr = requests.get('http://10.50.91.23:5000/palautus')
        print(rr.text, file=sys.stderr)
        flash(rr.text, category='info')
    return home()
    

            



if __name__ == '__main__':
    app.run(debug=True, port = 8080, host='0.0.0.0')