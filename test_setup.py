from langchain_ollama import ChatOllama

llm = ChatOllama(model="llama3.1")

resposta = llm.invoke("Diga apenas: funcionando!")
print(resposta.content)