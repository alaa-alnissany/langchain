from itertools import chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain_core.messages import SystemMessage, HumanMessage



try:
    from dotenv import load_dotenv
    load_dotenv(dotenv_path="../")
except ImportError:
    pass



# ------------------Using Template--------------------------
# This way can output just HumanMessage
template= """translate the following from english into {lang}:
            {q}"""
prompt= ChatPromptTemplate.from_template(template)


# ------------------Using message---------------------------
# This way can output both SystemMessage & HumanMessage
sys_message= "translate the following from english into {lang}"
# prompt definition in langchain site, we notice that .to_message() func is useless 
# prompt = ChatPromptTemplate.from_messages([
#      ("system", message),
#      ("user","{q}"),
#      ]).invoke({"q":"The part of speech used to indicate nouns and to specify their application.","lang":"Arabic"}).to_messages()

prompt = ChatPromptTemplate.from_messages([
     ("system", sys_message), # roles: system, user, ai, assistant, tool
     ("user","{q}"),
     ])

print(prompt)
# Define the model
model = OllamaLLM(model="qwen3")
chain = prompt | model
print(chain.invoke({"q":"The part of speech used to indicate nouns and to specify their application.","lang":"Arabic"}))




# ----------Using SystemMessage & HumanMessage--------------
# This method take a static string inputs without being able to invoke any variable into the prompt
# from langchain_core.schema import SystemMessage, HumanMessage # this is the old way.
prompt = [
    SystemMessage(content= "translate the following from english into Arabic"),
    HumanMessage(content= "how are you?")
]

print(prompt)
model = OllamaLLM(model="qwen3")
print(model.invoke(prompt))