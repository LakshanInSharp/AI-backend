# routes/query_routes.py
from fastapi import APIRouter, HTTPException, UploadFile, File
from Services.PineconeDB import PineconeClient
from Services.Document_Handler import Document_Handler
import os
import dotenv
import io



# Load Environment Variables
dotenv.load_dotenv()

pdf_router = APIRouter()

Document_Handler = Document_Handler()
PineconeClient = PineconeClient(os.getenv("PINECONE_API"), os.getenv("PINECONE_INDEX"))

@pdf_router.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Invalid file format. Only PDF allowed.")
    
    print(f"Received file: {file.filename}")
    
    try:
        file_stream = io.BytesIO(await file.read())
        
        # Extract Text and Splits into Chunks in temporary memory
        splits = Document_Handler.document_splitter_from_stream(file_stream)
        
        try:
            # Upload to Pinecone
            PineconeClient.Upsert_data_to_pinecone(splits)
            return {"message": "Successfully uploaded to vector database"}
        except Exception as e:
            raise HTTPException(status_code=500, detail="File not Uploaded to Vector DB")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))