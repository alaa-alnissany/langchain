# import getpass
from itertools import chain
# import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
# from langchain.chat_models import init_chat_model


try:
    from dotenv import load_dotenv
    load_dotenv(dotenv_path="../")
except ImportError:
    pass

# if not os.environ.get("OPENAI_API_KEY"):
#     os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API Key: ")
# model = init_chat_model("gpt-4o-mini", model_provider="openai")
# model.invoke("hello, world!")

template= """SYSTEM MESSAGE : {sys_msg}
Query: {q}"""

prompt= ChatPromptTemplate.from_template(template)

model = OllamaLLM(model="qwen3")

chain = prompt | model
print(chain.invoke({"q":"who is bashar alasaad?","sys_msg":"translate this into arabic"}))
