import random
from langchain.chat_models import ChatOpenAI
from app.chat.models import ChatArgs
from app.chat.vector_stores import retrieval_map
from app.chat.memory import memory_map
from app.chat.llms import llm_map
from app.chat.chains.retrieval import StreamingConversationalRetrievalChain
from app.web.api import (
    get_conversation_components,
    set_conversation_components
)

def select_components(component_type: str, component_map, chat_args):
    component = get_conversation_components(
        chat_args.conversation_id
    )
    previous_component = component[component_type]

    if previous_component:
        builder = component_map[previous_component]
        return previous_component, builder(chat_args)
    else:
        random_name = random.choice(list(component_map.keys()))
        builder = component_map[random_name]
        return random_name, builder(chat_args)



def build_chat(chat_args: ChatArgs):

    retriever_name, retriever = select_components(
        "retriever",
        retrieval_map,
        chat_args
    )

    llm_name, llm = select_components(
        "llm",
        llm_map,
        chat_args
    )

    memory_name, memory = select_components(
        "memory",
        memory_map,
        chat_args
    )
    
    print(f"using, memory: {memory_name}, llm: {llm_name} and retriever: {retriever_name}")

    set_conversation_components(
        conversation_id=chat_args.conversation_id,
        retriever=retriever_name,
        llm=llm_name,
        memory=memory_name
    )

    condense_question_llm = ChatOpenAI(streaming=False)

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
