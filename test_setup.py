from langchain_ollama import ChatOllama

llm = ChatOllama(model="llama3.1")

resposta = llm.invoke("Diga apenas: Salve igao, tamo no ar!")
print(resposta.content)