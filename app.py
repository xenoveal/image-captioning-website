from flask import render_template, Flask
from controller.use_model import main 
import argparse
from gtts import gTTS

app = Flask(__name__)

@app.route("/")
def hello_world():
    img_path = 'static/png/example4.jpg'
    args = argparse.Namespace(image=img_path, encoder_path='models/encoder-5-3000.pkl', decoder_path='models/decoder-5-3000.pkl', vocab_path='data/vocab.pkl', embed_size=256, hidden_size=512, num_layers=1)
    sentence = main(args=args)
    sentence_to_read = sentence.split("<start> ")[1].split(" <end>")[0]
    myobj = gTTS(text=sentence_to_read, lang='en', slow=False)
    myobj.save("static/text2speech.mp3")
    return render_template("home.html", sentence=sentence, img_path=img_path)

# @app.route('/upload', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         f = request.files['the_file']
#         f.save('/var/www/uploads/uploaded_file.txt')