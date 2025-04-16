from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import tempfile
from io import BytesIO
import os
#If new Document Uploded This Class should be run


class Document_Handler():

    def __init__(self):
       
        pass
     
    def Documet_Splitter(self,file_path,chunk_size=1024,chunck_overlap=20):
        loader=PyPDFLoader(file_path)
        docs=loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunck_overlap)
        splits=text_splitter.split_documents(Docs)
        return splits

    
    


    def document_splitter_from_stream(self, file_stream, chunk_size=1024, chunk_overlap=20):
        """
        Split a PDF document from a file stream into chunks.
        
        Args:
            file_stream: A file-like object containing the PDF data
            chunk_size: Size of each text chunk
            chunk_overlap: Overlap between chunks
            
        Returns:
            List of document chunks
        """
        # Create a temporary file to work with PyPDFLoader
        # (since PyPDFLoader requires a file path)
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
            # Write the stream content to the temporary file
            temp_file.write(file_stream.read())
            temp_file_path = temp_file.name
        
        try:
            # Load the PDF from the temporary file
            loader = PyPDFLoader(temp_file_path)
            docs = loader.load()
            
            #Split the documents
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size, 
                chunk_overlap=chunk_overlap
            )
            
            splits = text_splitter.split_documents(docs)
            
            return docs
        
        finally:
            # Clean up the temporary file
            import os
            try:
                os.unlink(temp_file_path)
            except:
                pass