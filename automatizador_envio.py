from resumir_noticias import gerar_relatorio, salvar_relatorio
from mailsender import enviar_relatorio_por_email

if __name__ == "__main__":
    print("Iniciando com as notícias do dia Igao...")

    resumos = gerar_relatorio(quantidade=5)

    print("Espera mais um pouquinho, quase lá..")
    salvar_relatorio(resumos)

    print("Agora sim! enviando por email Broski...")
    enviar_relatorio_por_email("relatorio_noticias.txt")

    print("Relatório enviado com sucesso, Igao! Agora é hora do cafézinho, see ya!")