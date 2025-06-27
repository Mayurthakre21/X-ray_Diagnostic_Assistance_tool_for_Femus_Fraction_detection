from flask import Flask, request, jsonify, render_template
import requests
import cv2
import numpy as np
from PIL import Image
import io
import base64

app = Flask(__name__)

ROBOFLOW_API_KEY = "0yoHAjinCTNZvd3jjEsW"
ROBOFLOW_PROJECT = "femoral-fracture-detection-lolu2"
ROBOFLOW_VERSION = "11"
ROBOFLOW_JSON_URL = f"https://detect.roboflow.com/{ROBOFLOW_PROJECT}/{ROBOFLOW_VERSION}?api_key={ROBOFLOW_API_KEY}"

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    image_file = request.files['image']
    image_bytes = image_file.read()
    pil_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    np_image = np.array(pil_image)
    image = cv2.cvtColor(np_image, cv2.COLOR_RGB2BGR)

    # Send to Roboflow for prediction
    response = requests.post(
        ROBOFLOW_JSON_URL,
        files={"file": image_bytes},
        data={"name": image_file.filename}
    )

    predictions = response.json().get("predictions", [])

    explanation = ""

    for idx, pred in enumerate(predictions):
        x, y = int(pred['x']), int(pred['y'])
        w, h = int(pred['width']), int(pred['height'])
        class_name = pred['class'].strip().lower()
        confidence = int(pred['confidence'] * 100)

    # Determine color: red for fracture, green for normal
        if "fracture" in class_name:
            box_color = (0, 0, 255)     # Red in BGR
        else:
            box_color = (34, 139, 34)     # Green in BGR

        x1 = int(x - w / 2)
        y1 = int(y - h / 2)
        x2 = int(x + w / 2)
        y2 = int(y + h / 2)

    # Draw bounding box
        cv2.rectangle(image, (x1, y1), (x2, y2), box_color, 2)

    # Create label
        label = f"{pred['class']} {confidence}%"
        (label_width, label_height), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)

        label_y = y1 - 10 if y1 - label_height - 10 > 0 else y1 + label_height + 10

    # Draw label background
        cv2.rectangle(
            image,
            (x1, label_y - label_height - 4),
            (x1 + label_width + 4, label_y + baseline),
            box_color,
            cv2.FILLED
        )

    # Draw white label text
        cv2.putText(
            image,
            label,
            (x1 + 2, label_y - 4),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),  # White text
            2
        )

    # Add explanation

    # Add to explanation
        explanation += f"{idx+1}. {class_name} detected with {confidence}% confidence.\n"


    # Encode final image
    _, buffer = cv2.imencode(".jpg", image)
    encoded_image = base64.b64encode(buffer).decode("utf-8")
    image_data_url = f"data:image/jpeg;base64,{encoded_image}"

    return jsonify({
        "annotated_image": image_data_url,
        "explanation": explanation or "No objects detected."
    })

if __name__ == "__main__":
    app.run(debug=True)
