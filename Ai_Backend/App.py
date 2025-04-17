# app.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import dotenv
import os
import logging
from routes.query_routes import query_router
from routes.pdf_routes import pdf_router

# Configure logging
logging.basicConfig(
    filename='app.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Load Environment Variables
dotenv.load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME")
PINECONE_API = os.getenv("PINECONE_API")
PINECONE_INDEX = os.getenv("PINECONE_INDEX")


def create_app():
    app = FastAPI(title="AI Backend API")
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(query_router, prefix="/api")
    app.include_router(pdf_router, prefix="/api")
    
    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)