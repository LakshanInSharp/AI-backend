
# routes/query_routes.py
from flask import Blueprint, request, jsonify
from Services.PineconeDB import PineconeClient
from Services.Document_Handler import Document_Handler
import os
import dotenv
import io



# Load Environment Variables
dotenv.load_dotenv()

pdf_handler = Blueprint('pdf', __name__)

Document_Handler=Document_Handler()
PineconeClient=PineconeClient(os.getenv("PINECONE_API"), os.getenv("PINECONE_INDEX"))


@pdf_handler.route('/upload-pdf', methods=['POST'])
def upload_pdf():
  

    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
        
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    print(f"Received file: {file.filename}")
    
    if file and file.filename.endswith('.pdf'):
        file_stream = io.BytesIO(file.read())

        # Extract Text and Splits into Chuncks in temprory memory pdf
        
        splits = Document_Handler.document_splitter_from_stream(file_stream)
  
  
        
        try:
            # Upload to Pinecone
            PineconeClient.Upsert_data_to_pinecone(splits)
            return jsonify({"message": "Successfully uploaded to vector database"}), 200
        except Exception as e:
            # If upload fails, return the text instead
            return jsonify({"message":"File not Uploded to Vector DB"}), 500
            
    
    return jsonify({'error': 'Invalid file format. Only PDF allowed.'}), 400