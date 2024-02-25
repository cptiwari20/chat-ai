from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.base import BaseCallbackHandler
from dotenv import load_dotenv
from queue import Queue
from threading import Thread

load_dotenv()

class HandleStreaming(BaseCallbackHandler):
    def __init__(self, queue) -> None:
        self.queue = queue

    def on_llm_new_token(self, token, **kwargs):
        self.queue.put(token)

    def on_llm_end(self, response, **kwargs):
        self.queue.put(None)

    def on_llm_error(self, error):
        self.queue.put(None)

chat = ChatOpenAI(
    streaming=True, #this allows OpenAI to send data to Langchain in streaming format.
    )

prompt = ChatPromptTemplate.from_messages([
    ('human', "{content}")
])

class StreamingChain(LLMChain):

    def stream(self, input):
        queue = Queue()
        handler = HandleStreaming(queue)

        def task():
            self(input, callbacks=[handler])
        
        Thread(target=task).start() #for running the concurrent process

        while True: #keep running the loop
            token = queue.get() # get the token from the process
            if(token is None): #break the loop
                break
            yield token #add the token to the process

chain = StreamingChain(llm=chat, prompt=prompt)


for chunk in chain.stream(input={"content":"tell me one fantastic joke in 200 words"}):
    print(chunk)
# messages = prompt.format_messages(content="Tell me a joke")

# for output in chat.stream(messages):
#     print(output.content)

