from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

try:
    embeddings = OllamaEmbeddings(
        model="nomic-embed-text",
    )
except Exception as e:
    print(e)

class ChromaDB():

    def __init__(self):
        pass


    def Create_Chroma(self,collection_name,embedding_function,persist_directory):
        
        vector_store = Chroma (
        collection_name=collection_name,
        embedding_function=embedding_function,
        persist_directory=persist_directory # Where to save data locally, remove if not necessary
         )
        
        return vector_store
    

    #Load Existing Chroma Database
    def Load_Chroma(self,embedding_function,persist_directory):
        
        vector_store = Chroma (
        embedding_function=embedding_function,
        persist_directory=persist_directory
         )
        
        return vector_store
    



    def Add_Documents_to_Chroma(self,vector_store,documents):
        """
        args: documents-->list
              ids--->unique id list
        
              
        """
        vector_store.add_documents(documents=documents)



    # def Transform_Vector_Store_into_Retriver(vector_store,search_type="mmr",top_k=1,fetch_k=20):
    #     retriever = vector_store.as_retriever(
    #     search_type=search_type, search_kwargs={"k": top_k, "fetch_k": fetch_k}
    #      )
        
    #     return retriever


Chromadb=ChromaDB()
Vector_Store=Chromadb.Create_Chroma("RAG_TEST",embeddings,"./Chroma_DB")
