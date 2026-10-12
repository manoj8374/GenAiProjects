from dotenv import load_dotenv
import chromadb
import textwrap
import io
from markitdown import MarkItDown
import hashlib
import uuid
load_dotenv()

md = MarkItDown()

class chromaWrap:
    def __init__(self, collection_name):
        self.client = chromadb.PersistentClient(path='./chroma_db') 
        self.collection_name = collection_name
        self.current_collection = self.client.get_or_create_collection(collection_name)
        self.docs = []

    def ingestion(self, documents):
        self.reset()
        ids = [str(uuid.uuid4()) for _ in documents]
        self.docs = documents
        self.current_collection.upsert(
            ids=ids,
            documents = self.docs
        )

    def process_ingest_docs(self, uploaded_files):
        all_chunks = []
        for file in uploaded_files:
            result = md.convert_stream(
                io.BytesIO(file.getvalue()),
                file_extension="." + file.name.rsplit(".", 1)[-1].lower(),
            )
            chunks = self.split_text(result.text_content)
            print("Chunks: ", len(chunks))
            all_chunks.extend(chunks)

        self.ingestion(all_chunks)

    def split_text(self, text, chunk_size=500):
        chunks = textwrap.wrap(
            text,
            width=chunk_size,
            break_long_words=False,
            break_on_hyphens=False
        )

        return chunks


    def query(self, query, k):
        result = self.current_collection.query(
            n_results = k,
            query_texts=[query]
        )
        return result

    def reset(self):
        self.client.delete_collection(self.collection_name)
        self.current_collection = self.client.get_or_create_collection(self.collection_name)