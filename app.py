from flask import Flask, render_template, request
import cv2
import os

app = Flask(__name__)

UPLOAD_FOLDER = "static"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return open("index.html").read()

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["image"]
    operation = request.form["operation"]

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    img = cv2.imread(filepath)

    # Apply operations
    if operation == "gray":
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    elif operation == "blur":
        img = cv2.GaussianBlur(img, (15, 15), 0)

    elif operation == "edge":
        img = cv2.Canny(img, 100, 200)

    elif operation == "invert":
        img = cv2.bitwise_not(img)

    output_path = os.path.join(UPLOAD_FOLDER, "output.jpg")
    cv2.imwrite(output_path, img)

    return f"<h2>Processed Image:</h2><img src='/{output_path}' width='300'>"

if __name__ == "__main__":
    app.run(debug=True)