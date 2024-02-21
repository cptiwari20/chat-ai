from langchain.chains import ConversationalRetrievalChain
from app.chat.models import ChatArgs
from app.chat.vector_stores.pinecone import build_retriever
from app.chat.memory.sql_memory import build_memory
from app.chat.llms.chat_openai import build_llm



def build_chat(chat_args: ChatArgs):
    retriever = build_retriever(chat_args=chat_args)
    llm = build_llm(chat_args)
    memory = build_memory(chat_args)

    return ConversationalRetrievalChain(
        llm=llm,
        memory=memory,
        retriever=retriever
    )



    """
    :param chat_args: ChatArgs object containing
        conversation_id, pdf_id, metadata, and streaming flag.

    :return: A chain

    Example Usage:

        chain = build_chat(chat_args)
    """

    pass
