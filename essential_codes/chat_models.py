import getpass
import os
from langchain.chat_models import init_chat_model

if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API Key: ")


model = init_chat_model("gpt-4o-mini", model_provider="openai")

model.invoke("hello, world!")
