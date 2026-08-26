from langchain_ollama import ChatOllama     # type: ignore
from langchain.agents import create_agent   # type: ignore
from langchain_core.tools import tool   # type: ignore
from buscar_noticias import buscar_noticias as buscar_noticias_raw

llm = ChatOllama(model="llama3.1")


@tool
def buscar_noticias_brasil(quantidade: int = 5) -> str:
    """Busca as notícias mais recentes do G1 e entrega título, resumo e o link de cada uma delas."""
    noticias = buscar_noticias_raw("https://g1.globo.com/rss/g1/", quantidade=quantidade)
    
    texto = ""
    for n in noticias:
        texto += f"Título: {n['titulo']}\nResumo: {n['resumo']}\nLink: {n['link']}\n\n"
    
    return texto


@tool
def buscar_noticias_internacionais(quantidade: int = 5) -> str:
    """Busca as notícias mais recentes do New York Times e entrega título, resumo e o link de cada uma delas."""
    noticias = buscar_noticias_raw("https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml", quantidade=quantidade)
    
    texto = ""
    for n in noticias:
        texto += f"Título: {n['titulo']}\nResumo: {n['resumo']}\nLink: {n['link']}\n\n"
    
    return texto


agente = create_agent(llm, tools=[buscar_noticias_brasil, buscar_noticias_internacionais])


def limpar_preambulo(texto):
    """remove algumas das frases de introdução mais comuns que o modelo adiciona no inicio do texto, como "aqui estão" ou "segue o resumo"."""
    frases_preambulo = [
        "aqui estão",
        "aqui está",
        "segue",
        "abaixo estão",
        "abaixo está",
        "a seguir estão",
        "a seguir está",
        "aqui estão algumas",
        "essas são algumas",
        "estas são algumas",
        "aqui estão as",
    ]

    linhas = texto.strip().split("\n")
    primeira_linha = linhas[0].lower()
    
    for frase in frases_preambulo:
        if frase in primeira_linha:
            linhas = linhas[1:]
            break
    
    return "\n".join(linhas).strip()


if __name__ == "__main__":
    resposta = agente.invoke({
        "messages": [
            {"role": "system", "content": "Você é um agente profissional de notícias. Sempre entregue em português. Evite escrever frases introdutórias que narrem suas ações como: aqui estão ou segue o resumo, sempre responda em formato de lista numerada, com titulo e resumo da noticia, direto pelo conteúdo."},
            {"role": "user", "content": "Busque por 3 notícias brasileiras e 3 notícias internacionais relevantes, em diversas áreas e me entregue um resumo de cada uma delas ."}
        ]
    })
    
    texto_final = limpar_preambulo(resposta["messages"][-1].content)
    print(texto_final)