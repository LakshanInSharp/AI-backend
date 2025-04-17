# routes/query_routes.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from Services.PineconeDB import PineconeClient
from Services.Generate_Response import Generate_Response
import os
import dotenv


# Load Environment Variables
dotenv.load_dotenv()

query_router = APIRouter()

Response = Generate_Response()
Pinecone_client = PineconeClient(os.getenv("PINECONE_API"), os.getenv("PINECONE_INDEX"))

class QueryRequest(BaseModel):
    query: str

@query_router.post("/query")
async def process_query(request: QueryRequest):
    query = request.query
    
    # Retrieve relevant context from Pinecone
    print("Retrieving Relevant Context...")
    print(f"query:{query}")
    
    context = Pinecone_client.retrive_data_from_pincone(query, 10)
    print(context)
    
    if not context:
        raise HTTPException(status_code=404, detail="No relevant context found")
    
    print("Generating LLM Answer...")
    response = Response.generate_response_deepseek(context, query)
    
    return {"response": response}