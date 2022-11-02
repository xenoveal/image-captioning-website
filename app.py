import random
import string
from flask import render_template, Flask, flash, request, redirect, url_for
from controller.vocabulary import Vocabulary
from controller.use_model import main 
import argparse
from gtts import gTTS
from werkzeug.utils import secure_filename
import os
import requests

# MYDIR = os.path.dirname(__file__)
# UPLOAD_FOLDER = 'static/upload'
UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "asdfahjjkasdkfaciw12dca$!@#DDAC"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def download_data():
    if(not os.path.exists("data")):
        os.mkdir("data")
    if(not os.path.exists("data/vocab.pkl")):
        response = requests.get("https://drive.google.com/uc?export=download&id=1M8biyGJEstcNKeO_ntpCH_qsW2k20BsT")
        open("data/vocab.pkl", "wb").write(response.content)
    if(not os.path.exists("models")):
        os.mkdir("models")
    if(not os.path.exists("models/decoder-5-3000.pkl")):
        response = requests.get("https://drive.google.com/uc?export=download&id=1thzppU7agKTL0yWqm1jBlGj6Gc8I4SUZ")
        open("models/decoder-5-3000.pkl", "wb").write(response.content)
    if(not os.path.exists("models/encoder-5-3000.pkl")):
        response = requests.get("https://drive.google.com/uc?export=download&id=14PxYQ0GIO2_5BYVfmDhnnyP4ALSoBcti")
        open("models/encoder-5-3000.pkl", "wb").write(response.content)

@app.route("/")
@app.route("/<string:img>")
def index(img=None):
    download_data()
    if(img):
        img = img.split("-")
        img_path = f"{app.config['UPLOAD_FOLDER']}/{img[1]}.{img[0]}"
        args = argparse.Namespace(image=img_path, encoder_path='models/encoder-5-3000.pkl', decoder_path='models/decoder-5-3000.pkl', vocab_path='data/vocab.pkl', embed_size=256, hidden_size=512, num_layers=1)
        sentence = main(args=args)
        sentence_to_read = sentence.split("<start> ")[1].split(" <end>")[0]
        myobj = gTTS(text=sentence_to_read, lang='en', slow=False)
        myobj.save("static/text2speech.mp3")
        return render_template("home.html", sentence=sentence_to_read, img_path=img_path)
    else:
        return render_template(
            "home.html", 
            sentence="Tap Twice to Upload Image and Tap Once to Play Sound"
        )

@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
        if file and allowed_file(file.filename):
            extension = secure_filename(file.filename).split('.')[-1]
            img_name = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
            img_path = f"{app.config['UPLOAD_FOLDER']}/{img_name}.{extension}"
            file.save(img_path)
            return redirect(url_for('index', img=f"{extension}-{img_name}"))
        return redirect('/')
    else:
        return redirect('/')