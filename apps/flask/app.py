from flask import Flask
from flask import request
from flask_cors import CORS
# from urllib.parse import unquote
# from werkzeug.utils import secure_filename



app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return 'Hello, World!'


@app.route("/api/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    if file:
      file.save("uploads/" + file.filename)
      return "success"
    else:
      return "failed"



if __name__ == '__main__':
    app.run()

