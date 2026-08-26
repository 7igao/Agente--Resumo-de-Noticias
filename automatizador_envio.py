import logging
from agent import agente, limpar_preambulo
from mailsender import enviar_relatorio_por_email

logging.basicConfig(
    filename='execucao.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

if __name__ == "__main__":
    try:
        logging.info("Iniciando com as notícias do dia Igao...")
        print("Iniciando com as notícias do dia Igao...")

        resposta = agente.invoke({
    "messages": [
        {"role": "system", "content": "Você é um agente de notícias. Sempre use as duas ferramentas disponíveis (Brasil e internacional) antes de responder. Responda sempre em português, direto com a lista de notícias numerada, sem comentários antes ou depois."},
        {"role": "user", "content": "Busque 3 notícias do Brasil e 3 notícias internacionais agora, e liste todas com título e resumo curto."}
    ]
})

        texto_final = limpar_preambulo(resposta["messages"][-1].content)

        logging.info("Salvando relatório em arquivo, Igao...")
        print("Espera mais um pouquinho, quase lá..")

        with open("relatorio_noticias.txt", "w", encoding="utf-8") as arquivo:
            arquivo.write(texto_final)

        logging.info("Enviando relatório por e-mail, Broski!...")
        print("Agora sim! enviando por email Broski...")
        enviar_relatorio_por_email("relatorio_noticias.txt")

        logging.info("Relatório enviado com sucesso")
        print("Relatório enviado com sucesso, Igao! Agora é hora do cafézinho, see ya!")

    except Exception as erro:
        logging.error(f"Ocorreu um erro: {erro}")
        print(f"Encontrei um erro que vale a pena debugar no code: {erro}")