
from pinecone import Pinecone, ServerlessSpec
import logging
import time
from datetime import datetime
import uuid

class PineconeClient():

    def __init__(self,API,index_name):
      
        self.pc=Pinecone(API)
        self.index_name=index_name



    def create_pinecone_index(self,dimension:int)->None:
        """
        creating pinecone database

        Args:
          dimension(int):Dimension of embedding model
        
        """
        self.pc.create_index(
            name=self.index_name,
            dimension=1024, 
            metric="cosine", # Replace with your model metric
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            ) 
        )
      

    def create_embedding(self,splits,model_name="multilingual-e5-large"):

        """create embeddings through pincone API
        
           Args:
           splits: Langchain splitted Chunks
        
        """

        embeddings = self.pc.inference.embed(
        model="multilingual-e5-large",
        inputs = [
                    d.page_content if hasattr(d, "page_content") else str(d)
                    for d in splits
                ],
        parameters={"input_type": "passage", "truncate": "END"})

        return embeddings




    # @staticmethod
    # def Generate_uids(num):
    #     """
    #     input--size of list

    #     output--list of UIDS
        
    #     """
    #     Uids=[]
    #     for i in range(num):
    #         random_uuid = uuid.uuid4()
    #         Uids.append(str(random_uuid))

    #     return Uids


    @staticmethod
    def generate_uids(num):
        """
        Generates a list of unique IDs.
        
        Parameters:
        - num: Number of UIDs to generate (int)
        
        Returns:
        - List of unique string IDs
        """
        uid_list = []
        for i in range(num):
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
            uid = f"{timestamp}_{i}_{uuid.uuid4().hex[:6]}"
            uid_list.append(uid)
        return uid_list



    def Upsert_data_to_pinecone(self, splits, embedding_model="multilingual-e5-large"):
        """
        When Input Splits It creates embeddings and stores them in Pinecone
        
        Args:
            splits: The document splits to embed and store
            embedding_model: The embedding model to use
        """

        logger = logging.getLogger(__name__)
        logger.info(f"Starting data upsert to Pinecone with {splits[4].page_content} splits using {embedding_model} model")
        
        try:
            logger.debug("Creating embeddings")
            embeddings = self.create_embedding(embedding_model, splits)
            logger.info(f"Successfully created {len(embeddings)} embeddings")
            
            logger.debug("Creating uids")
            uids=PineconeClient.generate_uids(len(embeddings))

            logger.info(f"Successfully created {len(uids)} uids")
            
            #Uids = Generate_uids(len(embeddings))
            #logger.debug(f"Generated {len(Uids)} unique IDs")
            
            # Wait for Pinecone index to be ready
            logger.info(f"Checking if index '{self.index_name}' is ready")
            while not self.pc.describe_index(self.index_name).status['ready']:
                logger.debug("Index not ready, waiting for 1 second")
                time.sleep(1)
            
            logger.info("Index is ready, preparing vectors for upload")
            index = self.pc.Index(self.index_name)
            
            vectors = []
            for d, e,id in zip(splits, embeddings,uids):
                vectors.append({
                    "id": id,
                    "values": e['values'],
                    "metadata": {'text': d.page_content}
                })
            
            logger.info(f"Upserting {len(vectors)} vectors to Pinecone index '{self.index_name}' in namespace 'ns1'")
            response = index.upsert(
                vectors=vectors,
                namespace="ns1"
            )
            
            logger.info(f"Successfully upserted data. Response: {response}")
            return response
         
            
        except Exception as e:
            logger.error(f"Error during Pinecone upsert: {str(e)}", exc_info=True)
            raise






    def retrive_data_from_pincone(self,query,top_k,model_name="multilingual-e5-large"):
        
        """Input-->user query
           Output-->Top_K Results
        
        
        """
        index = self.pc.Index(self.index_name)


        #embed input query
        embedding = self.pc.inference.embed(
        model="multilingual-e5-large",
        inputs=[query],
        parameters={
            "input_type": "query"
        } )

        #Retrive Top_k Results
        results = index.query(
        namespace="ns1",
        vector=embedding[0].values,
        top_k=top_k,
        include_values=False,
        include_metadata=True)


        #Concanate Results into paragaraph
        output=''
        for i in range(top_k):
            print("Scores:")
            print(results['matches'][i]['score'])

            if((results['matches'][i]['score'])>0.5):

                 output=output+"\n"+results['matches'][i]['metadata']['text']
        return output


        