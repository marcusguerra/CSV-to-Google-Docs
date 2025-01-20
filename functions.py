import pandas as pd
import re
from datetime import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow


def extrai_ID(link):
    # separa o link do google sheets em id e link
    padrao = r"(.*?/d/)([^/]+)/edit"
    correspondencia = re.search(padrao, link)
    if correspondencia:
        antes_do_id = correspondencia.group(1)
        id_planilha = correspondencia.group(2)
        return antes_do_id, id_planilha
    else:
        return None, None

def le_sheets(link):
    docs_link, id = extrai_ID(link)
    df = pd.read_csv(f"{docs_link}{id}/export?format=csv")
    return df



def autenticar_google_docs(credentials_path):
    SCOPES = ['https://www.googleapis.com/auth/documents']

    flow = InstalledAppFlow.from_client_secrets_file(
        credentials_path, SCOPES)
    creds = flow.run_local_server(port=0)

    service = build('docs', 'v1', credentials=creds)
    return service


def criar_documento(service, nome_documento):
    document = service.documents().create(body={'title': nome_documento}).execute()
    document_id = document['documentId']
    print(f'Documento criado com ID: {document_id} e Nome: {nome_documento}')
    return document_id


def adicionar_texto(service, document_id, texto):
    requests = []
    index = 1

    for texto_item, estilo in texto:
        if texto_item:  # Verificar se o texto não está vazio
            requests.append({
                'insertText': {
                    'location': {
                        'index': index,
                    },
                    'text': texto_item + '\n',
                }
            })

            # Atualizar estilo para o texto inserido
            requests.append({
                'updateTextStyle': {
                    'range': {
                        'startIndex': index,
                        'endIndex': index + len(texto_item),
                    },
                    'textStyle': estilo,
                    'fields': 'bold,fontSize,foregroundColor'
                }
            })


            index += len(texto_item) + 1

    service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()
    print('Texto formatado adicionado com sucesso!')


def processar_dataframe(df, CORES_STATUS):
    texto = []
    for status, cor in CORES_STATUS.items():
        projetos_status = df[df["Status do Projeto"] == status]
        # le o df e já coloca a cor nos status
        texto.append(formatar_texto_status(status, cor))
        for _, projeto in projetos_status.iterrows():
            texto.extend(formatar_texto_projeto(projeto))
            # pula uma linha
            texto.append((" ", {}))

    return texto

def formatar_texto_status(status, cor):
    #formata os 3 status possiveis por cor e tamanho
    return (status + ":", {
        'bold': True,
        'fontSize': {'magnitude': 16, 'unit': 'PT'},
        'foregroundColor': {'color': {'rgbColor': cor}}
    })

def formatar_texto_projeto(projeto):

    return [
        (projeto['Nome do Projeto'], {'bold': True, 'fontSize': {'magnitude': 14, 'unit': 'PT'}}),
        (f"Responsável: {projeto['Responsável']}", {'fontSize': {'magnitude': 10, 'unit': 'PT'}}),
        (f"Prazo Final: {projeto['Prazo Final']}", {'fontSize': {'magnitude': 10, 'unit': 'PT'}}),
        (f"Descrição: {projeto['Descrição do Projeto']}", {'fontSize': {'magnitude': 10, 'unit': 'PT'}}),
        (f"Observações: {projeto['Observações Adicionais']}", {'fontSize': {'magnitude': 10, 'unit': 'PT'}}),
        (f"Dias até Finalização: {projeto['Dias até Finalização']}", {'fontSize': {'magnitude': 10, 'unit': 'PT'}})
    ]

def gerar_nome_documento():
    data_atual = datetime.now().strftime("%d-%m-%Y")
    nome_documento = f"Project Briefing {data_atual}"
    return nome_documento

def sheets_to_docs(sheets_link, credentials_path, nome_docs=None):
    CORES_STATUS = {
        "Em andamento": {"red": 0, "green": 0, "blue": 1},
        "Pendente": {"red": 1, "green": 0, "blue": 0},
        "Concluído": {"red": 0, "green": 1, "blue": 0}
    }
    df = le_sheets(sheets_link)
    if nome_docs is None:
        nome_docs = gerar_nome_documento()
    service = autenticar_google_docs(credentials_path)
    document_id = criar_documento(service, nome_docs)
    texto = processar_dataframe(df, CORES_STATUS)
    adicionar_texto(service, document_id, texto)
