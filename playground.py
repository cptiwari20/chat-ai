from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.base import BaseCallbackHandler
from dotenv import load_dotenv

load_dotenv()

class HandleStreaming(BaseCallbackHandler):
    def on_llm_new_token(self, token, **kwargs):
        print(token)

chat = ChatOpenAI(
    streaming=True, #this allows OpenAI to send data to Langchain in streaming format.
    callbacks=[
        HandleStreaming() #this allows Langchain to handle streamed data handle.
        ]
    )

prompt = ChatPromptTemplate.from_messages([
    ('human', "{content}")
])

chain = LLMChain(llm=chat, prompt=prompt)


for chunk in chain.stream(input={"content":"tell me one fantastic joke"}):
    print(chunk)
# messages = prompt.format_messages(content="Tell me a joke")

# for output in chat.stream(messages):
#     print(output.content)

