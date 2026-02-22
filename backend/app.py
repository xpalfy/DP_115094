from flask import Flask
from flask_cors import CORS

from microservices.detect_routes import register_detect_routes
from microservices.average_images_routes import register_average_images_routes
from microservices.dataset_images_routes import register_dataset_images_routes

app = Flask(__name__)
CORS(app)

register_detect_routes(app)
register_average_images_routes(app)
register_dataset_images_routes(app)

if __name__ == "__main__":
    print("Flask API ready")
    app.run(host="0.0.0.0", port=5000, debug=True)