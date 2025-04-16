# routes/query_routes.py
from flask import Blueprint, request, jsonify
from Services.PineconeDB import PineconeClient
from Services.Generate_Response import Generate_Response
import os
import dotenv


# Load Environment Variables
dotenv.load_dotenv()

query_bp = Blueprint('query', __name__)

Response=Generate_Response()

# Initialize services
Pinecone_client = PineconeClient(os.getenv("PINECONE_API"), os.getenv("PINECONE_INDEX"))
# Response = Generate_Response()



@query_bp.route('/query', methods=['POST'])
def process_query():
    data = request.get_json()
    
    if not data or 'query' not in data:
        return jsonify({"error": "Missing query parameter"}), 400
    
    query = data['query']
    
    # Retrieve relevant context from Pinecone
    print("Retrieving Relevant Context...")
    print(f"query:{query}")
    
    #Query Expansion
    # query=Response.generate_response_common(query)

    context = Pinecone_client.retrive_data_from_pincone(query, 10)
    print(context)
    
    if not context:
        return jsonify({"error": "No relevant context found"}), 404
    
    print("Generating LLM Answer...")
    response = Response.generate_response_deepseek(context,query)
    
    return jsonify({"response": response})