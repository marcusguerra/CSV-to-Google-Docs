import pandas as pd
import re
import os
import google.auth
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow


def extrai_ID(link):
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

#le_sheets("https://docs.google.com/spreadsheets/d/1b5v4makJSmBwjxz7qk1uwJyDwQ04mN7tm3-dbumcpYQ/edit?gid=328103558#gid=328103558")


def autenticar_google_docs():
    SCOPES = ['https://www.googleapis.com/auth/documents']

    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)

    service = build('docs', 'v1', credentials=creds)
    return service


def criar_documento(service):
    document = service.documents().create().execute()
    document_id = document['documentId']
    print(f'Documento criado com ID: {document_id}')
    return document_id


def adicionar_texto(service, document_id, texto):
    requests = []

    for texto_item, estilo in texto:
        requests.append({
            'insertText': {
                'location': {
                    'index': 1,
                },
                'text': texto_item + '\n',
            }
        })

        requests.append({
            'updateTextStyle': {
                'range': {
                    'startIndex': 1,
                    'endIndex': 1 + len(texto_item),
                },
                'textStyle': estilo,
                'fields': 'bold,fontSize,foregroundColor'
            }
        })

    service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()
    print('Texto formatado adicionado com sucesso!')

def main():
    service = autenticar_google_docs()

    document_id = criar_documento(service)

    texto = [
        ('Carnes:', {'bold': True, 'fontSize': {'magnitude': 16, 'unit': 'PT'},
                     'foregroundColor': {'color': {'rgbColor': {'red': 1, 'green': 0, 'blue': 0}}}}),
        ('- alcatra', {'fontSize': {'magnitude': 10, 'unit': 'PT'}}),
        ('- cupim', {'fontSize': {'magnitude': 10, 'unit': 'PT'}}),
        ('- picanha', {'fontSize': {'magnitude': 10, 'unit': 'PT'}}),

        ('Bebidas:', {'bold': True, 'fontSize': {'magnitude': 16, 'unit': 'PT'},
                      'foregroundColor': {'color': {'rgbColor': {'red': 1, 'green': 0, 'blue': 0}}}}),
        ('- Cerveja', {'fontSize': {'magnitude': 10, 'unit': 'PT'}}),
        ('- Agua', {'fontSize': {'magnitude': 10, 'unit': 'PT'}}),
        ('- Limonada', {'fontSize': {'magnitude': 10, 'unit': 'PT'}}),

        ('Atividades:', {'bold': True, 'fontSize': {'magnitude': 16, 'unit': 'PT'},
                         'foregroundColor': {'color': {'rgbColor': {'red': 1, 'green': 0, 'blue': 0}}}}),
        ('- Piscina', {'fontSize': {'magnitude': 10, 'unit': 'PT'}}),
        ('- Escalada', {'fontSize': {'magnitude': 10, 'unit': 'PT'}}),
        ('- Diversão', {'fontSize': {'magnitude': 10, 'unit': 'PT'}}),
    ]

    adicionar_texto(service, document_id, texto)

if __name__ == '__main__':
    main()
