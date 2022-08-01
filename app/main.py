from io import BytesIO
from flask import Flask, request, send_file
from flask_cors import CORS
from app.cut_image import shuffle_img
from PIL import Image

app = Flask(__name__)
CORS(app)

def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')

@app.route('/', methods=['GET', 'PUT'])
def get_data():
    file = Image.open(request.files["image"].stream)
   
    rows = int(request.form["rows"])
    cols = int(request.form["cols"])
    final = shuffle_img(file, rows, cols)
    
    print("iPhone" in request.headers.get('User-Agent'))
    print(bool(request.form["isPortrait"]))
    if "iPhone" in request.headers.get('User-Agent') and bool(request.form["isPortrait"]):
      final.rotate(270)

    return serve_pil_image(final)

