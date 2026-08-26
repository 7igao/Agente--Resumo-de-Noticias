from langchain_ollama import ChatOllama # type: ignore
from buscar_noticias import buscar_noticias
from datetime import datetime

llm=ChatOllama(model="llama3.1")

def resumir_texto(titulo, texto_original):
    prompt = f"""Você é um assistente de informações que resume notícias de forma clara, objetiva e rápida.

Resuma a notícia abaixo em no máximo 4 frases, use a linguagem portuguesa, sem dar opinião pessoal.

IMPORTANTE: Você é um agente de notícias, não deve inventar informações e muito menos se comunicar com o usuário, apenas resuma a notícia. Se não houver informações suficientes para fornecer um resumo, responda apenas: "Não há informações suficientes para fornecer um resumo."

Título: {titulo}
Texto: {texto_original}

Resumo:"""

    resposta = llm.invoke(prompt)
    return limpar_preambulo(resposta.content.strip())


def limpar_preambulo(texto):
    """Remove frases de introdução comuns que o modelo às vezes adiciona."""
    frases_preambulo = [
        "aqui está o resumo da notícia:",
        "aqui está um resumo da notícia em",
        "resumo:",
        "aqui está o resumo:",
    ]
    
    texto_limpo = texto.strip()
    texto_lower = texto_limpo.lower()
    
    for frase in frases_preambulo:
        if texto_lower.startswith(frase):
            texto_limpo = texto_limpo[len(frase):].strip()
            texto_lower = texto_limpo.lower()
    
    return texto_limpo

def tem_conteudo_suficiente(resumo):
    """Verifica se o resumo indica falta de informação."""
    frases_negativas = [
        "não há informações suficientes",
        "não há detalhes suficientes",
        "não há informações suficientes para fornecer um resumo",
    ]
    resumo_lower = resumo.lower()
    return not any(frase in resumo_lower for frase in frases_negativas) 

def gerar_relatorio(quantidade=5):
    noticias = buscar_noticias("https://g1.globo.com/rss/g1/", quantidade=quantidade)
    resumos_validos = []

    for noticia in noticias:
        resumo = resumir_texto(noticia["titulo"], noticia["resumo"])

        if tem_conteudo_suficiente(resumo):
            resumos_validos.append({
                "titulo": noticia["titulo"],
                "resumo": resumo,
                "link": noticia["link"]
            })
        else:
            print(f"Pulando (conteúdo insuficiente): {noticia['titulo']}")

    return resumos_validos

def salvar_relatorio(resumos, nome_arquivo="relatorio_noticias.txt"):
    data_hoje = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write(f"Relatório gerado em: {data_hoje}\n\n")

        for i, resumo in enumerate(resumos, start=1):
            arquivo.write(f"--- Notícia {i} ---\n")
            arquivo.write(f"Título: {resumo['titulo']}\n")
            arquivo.write(f"Resumo: {resumo['resumo']}\n")
            arquivo.write(f"Link: {resumo['link']}\n\n")


if __name__ == "__main__":
    resumos = gerar_relatorio(quantidade=5)
    salvar_relatorio(resumos)