from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
import os

from hr_assistant import config
from hr_assistant.embedding import get_embedding_model
from hr_assistant.logger  import get_logger

logger = get_logger(__name__) 

#build vector store
def build_vector_store(chunks):
    """Embed every chunks and build a searchablel FAISS index in memory."""
    logger.info("chunks are uploading to Qdrant collection",config.QDRANT_COLLECTION_NAME)
    embeddings_model = get_embedding_model()
    vector_store = QdrantVectorStore.from_documents(documents =chunks, 
                                                    embedding = embeddings_model,
                                                    url = config.QDRANT_URL,
                                                    api_key = config.QDRANT_API_KEY,
                                                    collection_name =config.QDRANT_COLLECTION_NAME
                                                    )
    return vector_store


def load_vector_store():
    """Load a Qdrant collection."""
    embeddings_model = get_embedding_model()
    logger.info("Loading the qdrant vector store...")
    return QdrantVectorStore.from_existing_collection(
                                            embedding = embeddings_model,
                                            url = config.QDRANT_URL,
                                            api_key = config.QDRANT_API_KEY,
                                            collection_name =config.QDRANT_COLLECTION_NAME
                                            )


def vector_store_exists() -> bool:
    """Check if a saved  Qdrant vector store already exists ."""
    client = QdrantClient(
        url = config.QDRANT_URL,
        api_key = config.QDRANT_API_KEY
    )
    return client.collection_exists(config.QDRANT_COLLECTION_NAME)


def get_retriever(vector_store, k:int = config.TOP_K_RESULTS):
    """ Turn a vector store into a retriever that returns the top-k matching chunks."""
    logger.info("Creating retriever...")
    return vector_store.as_retriever(search_kwargs = {"k":k})