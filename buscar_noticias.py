import feedparser
from bs4 import BeautifulSoup

URL_FEED = "https://g1.globo.com/rss/g1/"

def limpar_html(texto):
    """
    Remove tags HTML de um texto.
    """
    soup = BeautifulSoup(texto, "html.parser")
    return soup.get_text()

def buscar_noticias(url, quantidade=5):
    feed = feedparser.parse(url)
    noticias = []
    for entrada in feed.entries[:quantidade]:
        resumo_bruto = entrada.get("summary", "")
        noticias.append({
            "titulo": limpar_html(entrada.title),
            "resumo": limpar_html(resumo_bruto),
            "link": entrada.link
        })
    return noticias

if __name__ == "__main__":
    noticias = buscar_noticias(URL_FEED)
    for i, noticia in enumerate(noticias, start=1):
        print(f"\n--- Notícia {i} ---")
        print("Título:", noticia["titulo"])
        print("Resumo:", noticia["resumo"][:150], "...")
        print("Link:", noticia["link"])