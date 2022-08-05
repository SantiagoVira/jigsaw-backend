from io import BytesIO
from flask import Flask, request, send_file
from flask_cors import CORS
from app.cut_image import shuffle_img, cut_image
from app.to_gif import to_gif
from PIL import Image
import numpy as np

app = Flask(__name__)
CORS(app)

def serve_pil_image(pil_img):
  img_io = BytesIO()
  pil_img.save(img_io, 'JPEG', quality=70)
  img_io.seek(0)
  return send_file(img_io, mimetype='image/jpeg')

def serve_gif(frames, total_duration:int):
  img_io = BytesIO()
  print(total_duration)
  print(total_duration/len(frames))
  frames[0].save(img_io, 'GIF', quality=70, save_all=True, append_images=frames[1:], duration=total_duration/len(frames), loop=0)
  img_io.seek(0)
  return send_file(img_io, mimetype='image/gif')

@app.route('/original', methods=['GET', 'POST'])
def get_data():
  original_image = Image.open(request.files["image"].stream)
  turn =  str(original_image.width) != request.form["width"]
  
  rows = int(request.form["rows"])
  cols = int(request.form["cols"])
  final = cut_image(original_image, rows, cols, turn)

  return serve_pil_image(final)

@app.route('/animation', methods=['GET', 'POST'])
def get_gif():
  original_image = Image.open(request.files["image"].stream)
  rows = int(request.form["rows"])
  cols = int(request.form["cols"])
  turn =  str(original_image.width) != request.form["width"]
  duration = int(request.form["duration"])
  
  frames = to_gif(original_image, rows, cols, turn)

  return serve_gif(frames, duration)