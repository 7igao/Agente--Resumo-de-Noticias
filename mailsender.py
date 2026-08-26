import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE")
EMAIL_SENHA_APP = os.getenv("EMAIL_SENHA_APP")
EMAIL_DESTINATARIO = os.getenv("EMAIL_DESTINATARIO")


def enviar_relatorio_por_email(caminho_arquivo, assunto="Resumo de Notícias"):
    """Ler o conteúdo de um arquivo de relatório e enviar por email."""
    
    with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
        conteudo = arquivo.read()

    mensagem = MIMEMultipart()
    mensagem["From"] = EMAIL_REMETENTE
    mensagem["To"] = EMAIL_DESTINATARIO
    mensagem["Subject"] = assunto

    mensagem.attach(MIMEText(conteudo, "plain", "utf-8"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as servidor:
            servidor.starttls()
            servidor.login(EMAIL_REMETENTE, EMAIL_SENHA_APP)
            servidor.send_message(mensagem)
        print(f"✅ E-mail enviado com sucesso para {EMAIL_DESTINATARIO}")
    except Exception as erro:
        print(f"❌ Erro ao enviar e-mail: {erro}")


if __name__ == "__main__":
    enviar_relatorio_por_email("relatorio_noticias.txt")