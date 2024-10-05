
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import os
from langchain_core.documents import Document
from uuid import uuid4



class Memory:
    def __init__(self, region):
        self.memory = []
        embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
        #create folder if not present

        if not os.path.exists('./.cortesh/embeddings/'):
            os.makedirs('./.cortesh/embeddings/')
        self.store = Chroma(
            collection_name=region,
            embedding_function=embeddings,
            persist_directory="./.cortesh/embeddings/",  # Where to save data locally, remove if not necessary
        )


    def add(self, key, value):
        uuid = str(uuid4())
        document = Document( page_content=value, metadata={"key": key}, id=uuid, )
        self.store.add_documents(documents=[document], ids=[uuid])
        return uuid

    def update(self, address, key, value):
        document = Document( page_content=value, metadata={"key": key}, id=address, )
        self.store.update_documents(documents=[document], ids=[address])
        return address

    def find(self, query):
        
        results = self.store.similarity_search_with_score(query=query,k=20)
        filteredResults = []
        for doc, score in results:
            if doc is None  or doc.metadata is None:
                next
            
            filteredResults.append(doc)
            
        return filteredResults

        

