from io import BytesIO
from flask import Flask, request, send_file
from flask_cors import CORS
from app.cut_image import cut_image
from PIL import Image

app = Flask(__name__)
CORS(app)

def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, 'PNG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

@app.route('/', methods=['GET', 'PUT'])
def get_data():
    file = Image.open(request.files["image"].stream)
    rows = int(request.form["rows"])
    cols = int(request.form["cols"])
    final = cut_image(file, rows, cols)
    return serve_pil_image(final)

