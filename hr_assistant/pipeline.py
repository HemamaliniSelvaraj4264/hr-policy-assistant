from hr_assistant import config
from hr_assistant.agent import create_hr_agent
from hr_assistant.document_loader import load_document
from hr_assistant.llm import get_llm
from hr_assistant.splitter import split_into_chunks
from hr_assistant.tools import create_search_tool
from hr_assistant.guardrails import REFUSAL_MESSAGE, check_input,check_output
from hr_assistant.vector_store import (
    build_vector_store,
    get_retriever,
    load_vector_store,
    vector_store_exists,
)
from hr_assistant.logger  import get_logger

logger = get_logger(__name__) 

def build_vector_store_for_document(file_path:str = config.DATA_FILE_PATH):
    if vector_store_exists():
        print("Found a saved vector store Qdrant Cloud")
        logger.info("Found a saved vector store  Qdrant cloud")
        return load_vector_store()
    
    print("No saved vector store found, building one from scratch..")
    logger.info("No saved vector store found, building one from scratch..")
    documents = load_document(file_path)
    chunks = split_into_chunks(documents)
    print(f"Loaded {file_path} and split it into {len(chunks)} chunks.")

    vector_store = build_vector_store(chunks)
    print("Vector store built and saved to disk")
    return vector_store



def build_hr_assistant(file_path: str = config.DATA_FILE_PATH):
    """Build the full RAG Agent, ready to answer question."""
    logger.info(" HR Assistant is building...")
    vector_store = build_vector_store_for_document(file_path)
    retriever = get_retriever(vector_store)
    search_tool = create_search_tool(retriever)

    llm = get_llm()
    agent = create_hr_agent(llm,[search_tool])

    logger.info("HR assistant is ready...")

    return agent

def ask(agent, question:str) -> str:
    """Ask the agent a question and return its final answer as plain text."""

    input_is_safe,_ = check_input(question)
    if not input_is_safe:
        return REFUSAL_MESSAGE
    response = agent.invoke({"messages":[{"role":"user","content":question}]})
    answer = response["messages"][-1].content
    logger.info("Final answer: %s",answer)

    output_is_safe,_=check_output(answer)
    if not output_is_safe:
        return REFUSAL_MESSAGE

    return answer