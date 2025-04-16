from Services.Document_Handler import Document_Handler
from Services.PineconeDB import PineconeClient
from Services.Generate_Response import Generate_Response

from langchain_ollama.llms import OllamaLLM
import dotenv
import os


#Load Environment Variables
dotenv.load_dotenv()
MODEL_NAME=os.getenv("MODEL_NAME")
PINECONE_API=os.getenv("PINECONE_API")
PINECONE_INDEX=os.getenv("PINECONE_INDEX")


#Initialize Objects
Document_Hanndle=Document_Handler()
Pinecone_client=PineconeClient(PINECONE_API,PINECONE_INDEX)
Response=Generate_Response()






#Input User Query
query=input("Enter Query:")

#Embed and retrive Relevant Context
print("Retreving Relevent Context......")
context=Pinecone_client.retrive_data_from_pincone(query,5)
print(context)
print("\n")



#Genearate Answers from LLM
print("Genrate LLM Answer......")



# while(True):
#response=Response.generate_response(input=query,context=context,model_name=MODEL_NAME)
response=Response.generate_response_deepseek(context)

        #score=Response.Relevance_Check(query,response)
        # print(f"score:{score}")
        # if(score[0]>0.5):

print(response)
        # break
  


