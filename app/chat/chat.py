from langchain.chat_models import ChatOpenAI
from app.chat.models import ChatArgs
from app.chat.vector_stores.pinecone import build_retriever
from app.chat.memory.sql_memory import build_memory
from app.chat.llms.chat_openai import build_llm
from app.chat.chains.retrieval import StreamingConversationalRetrievalChain



def build_chat(chat_args: ChatArgs):
    retriever = build_retriever(chat_args=chat_args)
    llm = build_llm(chat_args)
    condense_question_llm = ChatOpenAI(streaming=False)
    memory = build_memory(chat_args)

    # base_combine_doc = BaseCombineDocumentsChain()

    return StreamingConversationalRetrievalChain.from_llm(
        condense_question_llm=condense_question_llm, #second chain that will not stream
        # combine_docs_chain=base_combine_doc,
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
