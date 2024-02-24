from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

chat = ChatOpenAI()

prompt = ChatPromptTemplate.from_messages([
    ('human', "{content}")
])

messages = prompt.format_messages(content="Tell me a joke")

for output in chat.stream(messages):
    print(output.content)

