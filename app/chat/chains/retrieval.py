from langchain.chains import ConversationalRetrievalChain
from app.chat.chains.streamable import StreamableChain
from app.chat.chains.tracable import TracableChain

class StreamingConversationalRetrievalChain(
    TracableChain, StreamableChain, ConversationalRetrievalChain
):
    pass