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


