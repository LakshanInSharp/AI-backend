# app.py
from flask import Flask
import dotenv
import os
from routes.query_routes import query_bp
from routes.pdf_routes import pdf_handler

from flask_cors import CORS

import logging

logging.basicConfig(
    filename='app.log',  # This will create app.log file in the current directory
    level=logging.DEBUG,  # Capture all logs (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


# Load Environment Variables
dotenv.load_dotenv()


MODEL_NAME = os.getenv("MODEL_NAME")
PINECONE_API = os.getenv("PINECONE_API")
PINECONE_INDEX = os.getenv("PINECONE_INDEX")


def create_app():
    app = Flask(__name__)
    
    CORS(app)
    # Register blueprints
    app.register_blueprint(query_bp)
    app.register_blueprint(pdf_handler)

    
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8000,debug=True)