from langchain_text_splitters import RecursiveCharacterTextSplitter
from hr_assistant import config
from hr_assistant.logger  import get_logger

logger = get_logger(__name__) 

def split_into_chunks(documents):
    """Split documents into small overlappin chunks"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = config.chunk_size,
        chunk_overlap=config.chunk_overlap
    )
    chunks = text_splitter.split_documents(documents)
    logger.info("split document(s) into %d chunks(s)", len(chunks))
    return chunks