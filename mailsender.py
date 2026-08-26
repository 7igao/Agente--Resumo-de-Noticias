import resend
import os
from dotenv import load_dotenv

load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")
EMAIL_DESTINATARIO = os.getenv("EMAIL_DESTINATARIO")


def enviar_relatorio_por_email(caminho_arquivo, assunto="Resumo de Notícias"):
    """Ler o conteúdo de um arquivo relatório e enviar por email pelo Resend."""

    with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
        conteudo = arquivo.read()

    conteudo_html = conteudo.replace("\n", "<br>")

    try:
        resend.Emails.send({
            "from": "Agente de Notícias <onboarding@resend.dev>",
            "to": [EMAIL_DESTINATARIO],
            "subject": assunto,
            "html": conteudo_html,
        })
        print(f"✅ E-mail enviado com sucesso para {EMAIL_DESTINATARIO}")
    except Exception as erro:
        print(f"[X] Erro ao enviar e-mail: {erro}")


if __name__ == "__main__":
    enviar_relatorio_por_email("relatorio_noticias.txt")