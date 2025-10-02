#X-ray Diagnostic Assistance Tool for Femur Fracture Detection

Accurate and timely detection of femur fractures is crucial in medical diagnostics. Manual interpretation of X-ray images can be error-prone and time-consuming. This project aims to build a desktop-accessible web application that allows doctors to upload X-ray images, run them through a pre-trained object detection model, and receive automated predictions via an API.

🏗️ System Architecture
flowchart TD
    A[User Uploads X-ray] --> B[Flask Backend]
    B -->|Send Image| C[Roboflow API / Pre-trained Model]
    C -->|Prediction| B
    B --> D[Results Page on Browser]
    D --> E[Doctor/End User]

⚙️ Tech Stack

Frontend: HTML, CSS (Flask templates)

Backend: Flask (Python)

Model: Pre-trained object detection model (Roboflow API)

Tools: VS Code, Roboflow, Flask REST API


🧠 Deep Learning Model

Model Type: Pre-trained object detection (YOLOv5/EfficientDet, via Roboflow API)

Input Size: 416x416

Training Dataset: Femur X-ray dataset (fracture vs. normal)

Classes:

Fractured

Normal

Output: Bounding box with classification label + confidence score

📂 Project Structure
xray-fracture-detection/
│── static/           # CSS, JS, assets
│── templates/        # HTML templates
│── app.py            # Flask backend
│── model_api.py      # API integration with Roboflow
│── requirements.txt  # Python dependencies
│── README.md         # Documentation

🚀 How It Works

User uploads an X-ray image via web interface.

Flask backend sends the image to Roboflow API.

Pre-trained object detection model processes the image.

Results (fractured / normal + bounding box) are returned.

Prediction is displayed on browser.

🔧 Backend (Flask + API)

POST /upload → Accepts uploaded X-ray image, forwards to API.

GET /result → Displays prediction with annotated image.

API Response Example:

{
  "prediction": "Fractured",
  "confidence": 0.92,
  "bounding_box": [120, 45, 250, 300]
}

📊 Results

Detection Accuracy: [96%]

Example Output:
<img width="959" height="866" alt="image" src="https://github.com/user-attachments/assets/7f82a4e2-fe48-4f63-ad73-e7e54c87b555" />


📌 Future Scope

Expand to detect multiple bone fractures.

Support for X-ray/CT/MRI images.

Cloud deployment for multi-user access.

Integration with hospital PACS systems.

👨‍💻 Authors
Mayur Thakre – Backend + Model Integration + Frontend/UI, API setup

Dr. Vibha Bora - Guide

